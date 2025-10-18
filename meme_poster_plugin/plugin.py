"""
智能贴吧内容推送系统
根据配置自动获取指定贴吧内容，利用LLM进行智能评价和推送
支持多群组、多贴吧、随机时间推送等功能
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Tuple, Type, Optional, Dict, Any
from dataclasses import dataclass

import aiohttp
import base64
from PIL import Image
import io

from src.plugin_system import (
    BasePlugin, register_plugin, BaseAction, BaseCommand,
    ComponentInfo, ActionActivationType, ChatMode, ConfigField
)
from src.plugin_system.apis import database_api, llm_api, generator_api

# 导入自定义模块
from .tieba_crawler import TiebaCrawler, MockTiebaCrawler
from .meme_detector import MemeDetector, AdvancedMemeDetector
from .database_models import MemeSendRecords, MemeContentCache, MemeGroupSettings


class TiebaContentAction(BaseAction):
    """智能贴吧内容推送Action"""
    
    # === 基本信息 ===
    action_name = "tieba_content_action"
    action_description = "智能获取贴吧内容并进行LLM评价后推送"
    activation_type = ActionActivationType.RANDOM
    random_activation_probability = 0.03  # 3%概率激活
    mode_enable = ChatMode.ALL
    associated_types = ["image", "text"]
    parallel_action = False
    
    # === 功能描述 ===
    action_parameters = {
        "force_send": "是否强制发送（忽略限制）",
        "custom_message": "自定义发送消息",
        "target_tieba": "指定贴吧名称（可选）"
    }
    action_require = [
        "当需要推送有趣内容时使用",
        "当群组比较安静需要活跃气氛时使用",
        "当检测到群组适合推送贴吧内容时使用",
        "当需要分享有价值信息时使用"
    ]
    
    async def execute(self) -> Tuple[bool, str]:
        """执行智能贴吧内容推送"""
        try:
            # 检查是否启用插件
            if not self.get_config("plugin.enabled", False):
                return False, "插件未启用"
            
            # 检查是否在允许的群组中
            allowed_groups = self.get_config("posting.allowed_groups", [])
            if allowed_groups and self.group_id not in allowed_groups:
                return False, f"群组 {self.group_id} 不在允许列表中"
            
            # 检查今日发送次数限制
            force_send = self.action_data.get("force_send", False)
            if not force_send:
                if not await self._check_daily_limit():
                    return False, "今日发送次数已达上限"
            
            # 检查是否在推送时间范围内
            if not await self._check_push_time():
                return False, "不在推送时间范围内"
            
            # 获取贴吧数据
            target_tieba = self.action_data.get("target_tieba")
            tieba_data = await self._fetch_tieba_posts(target_tieba)
            if not tieba_data:
                return False, "获取贴吧数据失败"
            
            # 使用LLM评价内容
            evaluated_posts = await self._evaluate_posts_with_llm(tieba_data)
            if not evaluated_posts:
                return False, "未找到符合要求的内容"
            
            # 选择要发送的帖子
            selected_post = random.choice(evaluated_posts)
            
            # 发送内容
            success = await self._send_content(selected_post)
            
            if success:
                # 记录发送次数
                await self._record_send_count(selected_post)
                return True, f"成功推送内容: {selected_post.get('title', '无标题')}"
            else:
                return False, "推送内容失败"
                
        except Exception as e:
            print(f"执行贴吧内容推送时出错: {e}")
            import traceback
            traceback.print_exc()
            return False, f"执行贴吧内容推送时出错: {str(e)}"
    
    async def _check_daily_limit(self) -> bool:
        """检查今日发送次数限制"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            count = await database_api.db_query(
                MemeSendRecords,
                query_type="count",
                filters={
                    "group_id": self.group_id,
                    "send_date": today
                }
            )
            max_daily = self.get_config("posting.max_daily_sends", 3)
            return count < max_daily
        except Exception as e:
            print(f"检查每日限制时出错: {e}")
            return True  # 出错时允许发送，避免阻塞功能
    
    async def _check_push_time(self) -> bool:
        """检查是否在推送时间范围内"""
        try:
            # 获取推送时间配置
            push_hours = self.get_config("scheduling.push_hours", [9, 12, 15, 18, 21])  # 默认推送时间
            current_hour = datetime.now().hour
            
            # 检查当前时间是否在推送时间范围内
            if current_hour in push_hours:
                # 在推送时间范围内，随机决定是否推送
                push_probability = self.get_config("scheduling.push_probability", 0.3)
                return random.random() < push_probability
            
            return False
        except Exception as e:
            print(f"检查推送时间时出错: {e}")
            return True  # 出错时允许推送
    
    async def _fetch_tieba_posts(self, target_tieba: Optional[str] = None) -> Optional[List[Dict]]:
        """从贴吧获取帖子数据"""
        try:
            # 支持多贴吧配置
            if target_tieba:
                tieba_name = target_tieba
            else:
                tieba_list = self.get_config("tieba.tieba_list", ["搬石"])
                tieba_name = random.choice(tieba_list)
            
            fetch_count = self.get_config("tieba.fetch_count", 10)
            use_mock = self.get_config("tieba.use_mock", True)  # 默认使用模拟数据
            
            if use_mock:
                # 使用模拟爬虫
                crawler = MockTiebaCrawler()
            else:
                # 使用真实爬虫
                async with aiohttp.ClientSession() as session:
                    crawler = TiebaCrawler(session)
                    posts = await crawler.fetch_tieba_posts(tieba_name, count=fetch_count)
                    await crawler.close()
                    return posts
            
            # 获取帖子列表
            posts = await crawler.fetch_tieba_posts(tieba_name, count=fetch_count)
            
            # 获取帖子详情
            detailed_posts = []
            for post in posts:
                detail = await crawler.fetch_post_detail(post['url'])
                post.update(detail)
                detailed_posts.append(post)
            
            await crawler.close()
            return detailed_posts
            
        except Exception as e:
            print(f"获取贴吧数据失败: {e}")
            return None
    
    async def _evaluate_posts_with_llm(self, posts: List[Dict]) -> List[Dict]:
        """使用LLM评价帖子内容"""
        try:
            # 获取LLM模型配置
            available_models = llm_api.get_available_models()
            if not available_models:
                print("没有可用的LLM模型，使用基础过滤")
                return await self._filter_posts_basic(posts)
            
            # 选择第一个可用模型
            model_name = list(available_models.keys())[0]
            model_config = available_models[model_name]
            
            evaluated_posts = []
            
            for post in posts:
                try:
                    # 构建评价提示词
                    evaluation_prompt = self._build_evaluation_prompt(post)
                    
                    # 使用LLM评价
                    success, response, reasoning, model_used = await llm_api.generate_with_model(
                        prompt=evaluation_prompt,
                        model_config=model_config,
                        request_type="tieba_content_evaluation",
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    if success and response:
                        # 解析LLM评价结果
                        evaluation_result = self._parse_evaluation_response(response)
                        
                        if evaluation_result.get('should_send', False):
                            post['llm_evaluation'] = evaluation_result
                            post['content_type'] = evaluation_result.get('content_type', 'unknown')
                            post['interest_score'] = evaluation_result.get('interest_score', 0.5)
                            evaluated_posts.append(post)
                            
                except Exception as e:
                    print(f"评价帖子时出错: {e}")
                    continue
            
            # 按兴趣评分排序
            evaluated_posts.sort(key=lambda x: x.get('interest_score', 0), reverse=True)
            
            return evaluated_posts
            
        except Exception as e:
            print(f"LLM评价失败: {e}")
            # 回退到基础过滤
            return await self._filter_posts_basic(posts)
    
    def _build_evaluation_prompt(self, post: Dict) -> str:
        """构建LLM评价提示词"""
        title = post.get('title', '')
        content = post.get('content', '')
        images = post.get('images', [])
        reply_count = post.get('reply_count', 0)
        
        prompt = f"""
请评价以下贴吧帖子内容，判断是否适合推送到群聊中：

标题: {title}
内容: {content}
图片数量: {len(images)}
回复数: {reply_count}

请从以下角度进行评价：
1. 内容是否有趣或有用
2. 是否符合群聊氛围
3. 内容类型（meme梗图/二次元作品/信息分享/其他）
4. 兴趣评分（0-1分）

请以JSON格式回复：
{{
    "should_send": true/false,
    "content_type": "meme/artwork/information/other",
    "interest_score": 0.0-1.0,
    "reason": "评价理由"
}}
"""
        return prompt
    
    def _parse_evaluation_response(self, response: str) -> Dict:
        """解析LLM评价响应"""
        try:
            # 尝试解析JSON
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # 如果JSON解析失败，使用简单规则
        response_lower = response.lower()
        should_send = 'true' in response_lower or '是' in response_lower
        content_type = 'other'
        if 'meme' in response_lower or '梗图' in response_lower:
            content_type = 'meme'
        elif 'artwork' in response_lower or '二次元' in response_lower or '画师' in response_lower:
            content_type = 'artwork'
        elif 'information' in response_lower or '信息' in response_lower:
            content_type = 'information'
        
        # 提取评分
        score_match = re.search(r'(\d+\.?\d*)', response)
        interest_score = float(score_match.group(1)) if score_match else 0.5
        
        return {
            'should_send': should_send,
            'content_type': content_type,
            'interest_score': min(max(interest_score, 0.0), 1.0),
            'reason': response[:100] + '...' if len(response) > 100 else response
        }
    
    async def _filter_posts_basic(self, posts: List[Dict]) -> List[Dict]:
        """基础帖子过滤（LLM不可用时的回退方案）"""
        filtered_posts = []
        meme_keywords = self.get_config("filtering.meme_keywords", [
            "梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图"
        ])
        
        detector = MemeDetector()
        
        for post in posts:
            try:
                # 检查是否有图片
                images = post.get("images", [])
                if not images:
                    continue
                
                # 使用基础检测器判断
                is_meme, score = await detector.is_meme_content(post, meme_keywords)
                
                if is_meme and score >= 0.6:
                    post['content_type'] = 'meme'
                    post['interest_score'] = score
                    post['llm_evaluation'] = {
                        'should_send': True,
                        'content_type': 'meme',
                        'interest_score': score,
                        'reason': '基础检测通过'
                    }
                    filtered_posts.append(post)
                    
            except Exception as e:
                print(f"基础过滤帖子时出错: {e}")
                continue
        
        return filtered_posts
    
    async def _filter_meme_posts(self, posts: List[Dict]) -> List[Dict]:
        """筛选出包含meme图片的帖子"""
        meme_posts = []
        meme_keywords = self.get_config("filtering.meme_keywords", [
            "梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图"
        ])
        
        # 初始化meme检测器
        detector = MemeDetector()
        
        for post in posts:
            try:
                # 检查是否有图片
                images = post.get("images", [])
                if not images:
                    continue
                
                # 使用meme检测器判断
                is_meme, score = await detector.is_meme_content(post, meme_keywords)
                
                # 如果检测为meme，添加到结果列表
                if is_meme:
                    post['meme_score'] = score
                    meme_posts.append(post)
                
            except Exception as e:
                print(f"过滤帖子时出错: {e}")
                continue
        
        return meme_posts
    
    async def _send_content(self, post: Dict) -> bool:
        """发送内容到群组"""
        try:
            content_type = post.get('content_type', 'unknown')
            llm_eval = post.get('llm_evaluation', {})
            interest_score = post.get('interest_score', 0.5)
            
            # 根据内容类型决定发送方式
            if content_type in ['meme', 'artwork']:
                # 对于meme和二次元作品，直接推送图片
                return await self._send_image_content(post)
            else:
                # 对于其他内容，使用LLM生成描述
                return await self._send_described_content(post)
                
        except Exception as e:
            print(f"发送内容失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _send_image_content(self, post: Dict) -> bool:
        """发送图片内容（meme或二次元作品）"""
        try:
            # 发送简单的文本描述
            title = post.get('title', '有趣的图片')
            content_type = post.get('content_type', 'unknown')
            
            if content_type == 'meme':
                text_content = f"🎭 {title}"
            elif content_type == 'artwork':
                text_content = f"🎨 {title}"
            else:
                text_content = f"📸 {title}"
            
            text_success = await self.send_text(text_content)
            
            # 发送图片
            image_success = True
            if post.get("images"):
                # 创建模拟图片（实际实现中应该下载真实图片）
                detector = MemeDetector()
                mock_image_data = await detector.create_mock_meme_image(title)
                mock_image_base64 = base64.b64encode(mock_image_data).decode('utf-8')
                image_success = await self.send_image(mock_image_base64)
            
            return text_success and image_success
            
        except Exception as e:
            print(f"发送图片内容失败: {e}")
            return False
    
    async def _send_described_content(self, post: Dict) -> bool:
        """发送带LLM描述的内容"""
        try:
            # 使用Generator API生成描述
            title = post.get('title', '')
            content = post.get('content', '')
            llm_eval = post.get('llm_evaluation', {})
            
            # 构建描述提示词
            description_prompt = f"""
请为以下贴吧内容生成一个有趣的群聊描述：

标题: {title}
内容: {content}
内容类型: {llm_eval.get('content_type', 'unknown')}
兴趣评分: {llm_eval.get('interest_score', 0.5)}

要求：
1. 语言要生动有趣，符合群聊氛围
2. 长度控制在50字以内
3. 可以适当添加表情符号
4. 突出内容的亮点

请直接输出描述内容，不要其他格式。
"""
            
            # 使用Generator API生成描述
            description = await generator_api.generate_response_custom(
                chat_stream=self.chat_stream,
                prompt=description_prompt
            )
            
            if not description:
                # 回退到简单描述
                description = f"📝 {title}\n\n{content[:100]}{'...' if len(content) > 100 else ''}"
            
            # 发送描述
            text_success = await self.send_text(description)
            
            # 如果有图片，也发送图片
            image_success = True
            if post.get("images"):
                detector = MemeDetector()
                mock_image_data = await detector.create_mock_meme_image(title)
                mock_image_base64 = base64.b64encode(mock_image_data).decode('utf-8')
                image_success = await self.send_image(mock_image_base64)
            
            return text_success and image_success
            
        except Exception as e:
            print(f"发送描述内容失败: {e}")
            # 回退到简单发送
            return await self._send_image_content(post)
    
    
    async def _record_send_count(self, post: Dict):
        """记录发送次数"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            await database_api.db_query(
                MemeSendRecords,
                data={
                    "group_id": self.group_id,
                    "group_name": self.group_name,
                    "send_date": today,
                    "send_time": datetime.now().isoformat(),
                    "post_title": post.get('title', '未知标题'),
                    "post_content": post.get('content', ''),
                    "post_author": post.get('author', '未知作者'),
                    "image_count": len(post.get('images', [])),
                    "send_success": True
                },
                query_type="create"
            )
        except Exception as e:
            print(f"记录发送次数失败: {e}")


class TiebaStatusCommand(BaseCommand):
    """贴吧内容推送状态查询命令"""
    
    command_name = "tieba_status"
    command_description = "查看贴吧内容推送状态和统计信息"
    command_pattern = r"^/tieba_status$"
    
    async def execute(self) -> Tuple[bool, str, bool]:
        """执行状态查询"""
        try:
            # 检查是否启用插件
            if not self.get_config("plugin.enabled", False):
                await self.send_text("❌ 贴吧内容推送插件未启用")
                return True, "插件未启用", True
            
            # 获取群组信息（从消息中获取）
            group_id = getattr(self, 'group_id', 'unknown')
            group_name = getattr(self, 'group_name', '未知群组')
            
            # 获取今日发送次数
            today = datetime.now().strftime("%Y-%m-%d")
            try:
                today_count = await database_api.db_query(
                    MemeSendRecords,
                    query_type="count",
                    filters={
                        "group_id": group_id,
                        "send_date": today
                    }
                )
            except Exception as e:
                print(f"获取发送次数失败: {e}")
                today_count = 0
            
            # 获取配置信息
            max_daily = self.get_config("posting.max_daily_sends", 3)
            tieba_list = self.get_config("tieba.tieba_list", ["搬石"])
            push_hours = self.get_config("scheduling.push_hours", [9, 12, 15, 18, 21])
            push_probability = self.get_config("scheduling.push_probability", 0.3)
            
            # 构建状态消息
            status_message = f"""📊 **贴吧内容推送状态报告**

🏷️ **群组**: {group_name}
📅 **日期**: {today}
📈 **今日发送**: {today_count}/{max_daily}
🎯 **目标贴吧**: {', '.join(tieba_list)}
⏰ **推送时间**: {', '.join(map(str, push_hours))}点
🎲 **推送概率**: {push_probability*100:.0f}%
⚙️ **插件状态**: {'✅ 启用' if self.get_config('plugin.enabled', False) else '❌ 禁用'}

💡 **功能说明**:
- 智能获取贴吧内容并进行LLM评价
- 支持多贴吧随机选择
- 随机时间推送，符合人类作息
- 自动识别内容类型（meme/二次元/信息等）
- 每日最多发送 {max_daily} 次"""
            
            await self.send_text(status_message)
            return True, f"显示了贴吧推送状态信息", True
            
        except Exception as e:
            await self.send_text(f"❌ 查询状态失败: {str(e)}")
            return False, f"查询失败: {str(e)}", True


class TiebaConfigCommand(BaseCommand):
    """贴吧推送配置管理命令"""
    
    command_name = "tieba_config"
    command_description = "管理贴吧推送配置"
    command_pattern = r"^/tieba_config\s+(?P<action>\w+)(?:\s+(?P<param>.*))?$"
    
    async def execute(self) -> Tuple[bool, str, bool]:
        """执行配置管理"""
        try:
            action = self.matched_groups.get("action", "").lower()
            param = self.matched_groups.get("param")
            
            # 安全处理param参数
            if param is not None:
                param = param.strip()
            else:
                param = ""
            
            if action == "list":
                return await self._list_config()
            elif action == "set":
                return await self._set_config(param)
            elif action == "help":
                return await self._show_help()
            else:
                await self.send_text("❌ 未知操作，使用 /tieba_config help 查看帮助")
                return False, "未知操作", True
                
        except Exception as e:
            await self.send_text(f"❌ 配置管理失败: {str(e)}")
            return False, f"配置管理失败: {str(e)}", True
    
    async def _list_config(self) -> Tuple[bool, str, bool]:
        """列出当前配置"""
        try:
            # 获取当前配置
            enabled = self.get_config("plugin.enabled", False)
            tieba_list = self.get_config("tieba.tieba_list", ["搬石"])
            max_daily = self.get_config("posting.max_daily_sends", 3)
            push_hours = self.get_config("scheduling.push_hours", [9, 12, 15, 18, 21])
            push_probability = self.get_config("scheduling.push_probability", 0.3)
            llm_enabled = self.get_config("llm.enable_llm_evaluation", True)
            
            config_message = f"""📋 **当前配置**

🔧 **基本设置**:
- 插件状态: {'✅ 启用' if enabled else '❌ 禁用'}
- 每日最大发送: {max_daily} 次
- LLM评价: {'✅ 启用' if llm_enabled else '❌ 禁用'}

🎯 **贴吧设置**:
- 目标贴吧: {', '.join(tieba_list)}

⏰ **推送设置**:
- 推送时间: {', '.join(map(str, push_hours))}点
- 推送概率: {push_probability*100:.0f}%

💡 **使用 /tieba_config help 查看配置命令**"""
            
            await self.send_text(config_message)
            return True, "显示了当前配置", True
            
        except Exception as e:
            await self.send_text(f"❌ 获取配置失败: {str(e)}")
            return False, f"获取配置失败: {str(e)}", True
    
    async def _set_config(self, param: str) -> Tuple[bool, str, bool]:
        """设置配置"""
        try:
            if not param:
                await self.send_text("❌ 请提供配置参数，使用 /tieba_config help 查看帮助")
                return False, "缺少参数", True
            
            # 解析配置参数
            parts = param.split("=", 1)
            if len(parts) != 2:
                await self.send_text("❌ 配置格式错误，应为 key=value")
                return False, "格式错误", True
            
            key, value = parts[0].strip(), parts[1].strip()
            
            # 这里只是显示，实际配置需要通过配置文件修改
            await self.send_text(f"⚠️ 配置修改功能暂未实现\n\n要修改配置，请编辑插件的 config.toml 文件：\n- 配置项: {key}\n- 新值: {value}\n\n修改后请重启插件。")
            return True, f"显示了配置修改信息: {key}={value}", True
            
        except Exception as e:
            await self.send_text(f"❌ 设置配置失败: {str(e)}")
            return False, f"设置配置失败: {str(e)}", True
    
    async def _show_help(self) -> Tuple[bool, str, bool]:
        """显示帮助信息"""
        help_message = """📖 **贴吧推送配置命令帮助**

🔧 **可用命令**:
- `/tieba_config list` - 查看当前配置
- `/tieba_config set key=value` - 设置配置（需要编辑配置文件）
- `/tieba_config help` - 显示此帮助

📋 **主要配置项**:
- `plugin.enabled` - 是否启用插件
- `tieba.tieba_list` - 目标贴吧列表
- `posting.max_daily_sends` - 每日最大发送次数
- `scheduling.push_hours` - 推送时间点
- `scheduling.push_probability` - 推送概率
- `llm.enable_llm_evaluation` - 是否启用LLM评价

💡 **注意**: 配置修改需要编辑 config.toml 文件并重启插件"""
        
        await self.send_text(help_message)
        return True, "显示了帮助信息", True


@register_plugin
class TiebaContentPlugin(BasePlugin):
    """智能贴吧内容推送系统"""
    
    # 插件基本信息
    plugin_name = "tieba_content_plugin"
    enable_plugin = True
    dependencies = []
    python_dependencies = ["aiohttp", "Pillow", "numpy"]
    config_file_name = "config.toml"
    
    def __init__(self):
        super().__init__()
        # 初始化数据库表
        self._init_database_tables()
    
    def _init_database_tables(self):
        """初始化数据库表"""
        try:
            from .database_models import MemeSendRecords, MemeContentCache, MemeGroupSettings
            
            # 创建数据库表（如果不存在）
            MemeSendRecords.create_table(safe=True)
            MemeContentCache.create_table(safe=True)
            MemeGroupSettings.create_table(safe=True)
            
            print("✅ 贴吧内容推送插件数据库表初始化成功")
        except Exception as e:
            print(f"❌ 数据库表初始化失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 配置节描述
    config_section_descriptions = {
        "plugin": "插件基本配置",
        "posting": "发送控制配置", 
        "tieba": "贴吧数据源配置",
        "filtering": "内容过滤配置",
        "scheduling": "定时任务配置",
        "llm": "LLM评价配置"
    }
    
    # 配置Schema定义
    config_schema = {
        "plugin": {
            "enabled": ConfigField(type=bool, default=False, description="是否启用插件"),
            "config_version": ConfigField(type=str, default="1.0.0", description="配置文件版本")
        },
        "posting": {
            "allowed_groups": ConfigField(
                type=list, 
                default=[], 
                description="允许发送的群组ID列表，为空表示所有群组",
                example=["123456789", "987654321"]
            ),
            "max_daily_sends": ConfigField(
                type=int, 
                default=3, 
                description="每日最大发送次数",
                example=5
            ),
            "send_interval_min": ConfigField(
                type=int, 
                default=30, 
                description="发送间隔（分钟）",
                example=60
            )
        },
        "tieba": {
            "tieba_list": ConfigField(
                type=list, 
                default=["搬石", "沙雕图", "二次元"], 
                description="目标贴吧名称列表",
                example=["搬石", "沙雕图", "二次元", "技术"]
            ),
            "fetch_count": ConfigField(
                type=int, 
                default=10, 
                description="每次获取的帖子数量",
                example=20
            ),
            "use_mock": ConfigField(
                type=bool,
                default=True,
                description="是否使用模拟数据（测试用）"
            ),
            "api_url": ConfigField(
                type=str, 
                default="", 
                description="贴吧API地址（可选）",
                example="https://api.tieba.com/posts"
            )
        },
        "filtering": {
            "meme_keywords": ConfigField(
                type=list,
                default=["梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图"],
                description="meme内容关键词列表",
                example=["梗图", "沙雕", "表情包"]
            ),
            "min_image_count": ConfigField(
                type=int,
                default=1,
                description="帖子最少图片数量",
                example=1
            )
        },
        "scheduling": {
            "enable_auto_send": ConfigField(
                type=bool,
                default=True,
                description="是否启用自动发送"
            ),
            "push_hours": ConfigField(
                type=list,
                default=[9, 12, 15, 18, 21],
                description="推送时间点（24小时制）",
                example=[9, 12, 15, 18, 21]
            ),
            "push_probability": ConfigField(
                type=float,
                default=0.3,
                description="推送概率（0-1）",
                example=0.3
            ),
            "check_interval": ConfigField(
                type=int,
                default=300,
                description="检查间隔（秒）",
                example=600
            )
        },
        "llm": {
            "enable_llm_evaluation": ConfigField(
                type=bool,
                default=True,
                description="是否启用LLM评价"
            ),
            "evaluation_model": ConfigField(
                type=str,
                default="",
                description="评价使用的模型名称（空则自动选择）",
                example="gpt-3.5-turbo"
            ),
            "min_interest_score": ConfigField(
                type=float,
                default=0.6,
                description="最低兴趣评分阈值",
                example=0.6
            )
        }
    }
    
    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        """返回插件包含的组件列表"""
        return [
            (TiebaContentAction.get_action_info(), TiebaContentAction),
            (TiebaStatusCommand.get_command_info(), TiebaStatusCommand),
            (TiebaConfigCommand.get_command_info(), TiebaConfigCommand),
        ]
