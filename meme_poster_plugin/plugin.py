"""
贴吧Meme梗图自动发送插件
自动从百度贴吧获取meme梗图并发送到指定群组
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
from src.plugin_system.apis import send_api, database_api

# 导入自定义模块
from .tieba_crawler import TiebaCrawler, MockTiebaCrawler
from .meme_detector import MemeDetector, AdvancedMemeDetector
from .database_models import MemeSendRecords, MemeContentCache, MemeGroupSettings


class MemePosterAction(BaseAction):
    """贴吧Meme梗图自动发送Action"""
    
    # === 基本信息 ===
    action_name = "meme_poster_action"
    action_description = "自动从贴吧获取meme梗图并发送到群组"
    activation_type = ActionActivationType.RANDOM
    random_activation_probability = 0.05  # 5%概率激活
    mode_enable = ChatMode.ALL
    associated_types = ["image", "text"]
    parallel_action = False
    
    # === 功能描述 ===
    action_parameters = {
        "force_send": "是否强制发送（忽略限制）",
        "custom_message": "自定义发送消息"
    }
    action_require = [
        "当需要发送有趣内容时使用",
        "当群组比较安静需要活跃气氛时使用",
        "当检测到群组适合发送meme内容时使用"
    ]
    
    async def execute(self) -> Tuple[bool, str]:
        """执行meme发送动作"""
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
            
            # 获取贴吧数据
            tieba_data = await self._fetch_tieba_posts()
            if not tieba_data:
                return False, "获取贴吧数据失败"
            
            # 筛选meme图片
            meme_posts = await self._filter_meme_posts(tieba_data)
            if not meme_posts:
                return False, "未找到合适的meme内容"
            
            # 选择要发送的帖子
            selected_post = random.choice(meme_posts)
            
            # 发送图片和文本
            success = await self._send_meme_content(selected_post)
            
            if success:
                # 记录发送次数
                await self._record_send_count()
                return True, f"成功发送meme内容: {selected_post.get('title', '无标题')}"
            else:
                return False, "发送meme内容失败"
                
        except Exception as e:
            return False, f"执行meme发送时出错: {str(e)}"
    
    async def _check_daily_limit(self) -> bool:
        """检查今日发送次数限制"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            count = await database_api.db_query(
                "MemeSendRecords",
                query_type="count",
                filters={
                    "group_id": self.group_id,
                    "send_date": today
                }
            )
            max_daily = self.get_config("posting.max_daily_sends", 3)
            return count < max_daily
        except:
            return True  # 出错时允许发送
    
    async def _fetch_tieba_posts(self) -> Optional[List[Dict]]:
        """从贴吧获取帖子数据"""
        try:
            tieba_name = self.get_config("tieba.tieba_name", "搬石")
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
    
    async def _send_meme_content(self, post: Dict) -> bool:
        """发送meme内容到群组"""
        try:
            # 发送文本消息
            custom_message = self.action_data.get("custom_message", "")
            if custom_message:
                text_content = custom_message
            else:
                meme_score = post.get('meme_score', 0)
                text_content = f"📸 {post.get('title', '有趣的图片')}\n\n{post.get('content', '')}\n\n🎯 Meme评分: {meme_score:.2f}"
            
            # 发送文本
            text_success = await self.send_text(text_content)
            
            # 发送图片
            image_success = True
            if post.get("images"):
                # 创建模拟图片（实际实现中应该下载真实图片）
                detector = MemeDetector()
                mock_image_data = await detector.create_mock_meme_image(post.get('title', 'Meme图片'))
                mock_image_base64 = base64.b64encode(mock_image_data).decode('utf-8')
                image_success = await self.send_image(mock_image_base64)
            
            return text_success and image_success
            
        except Exception as e:
            print(f"发送meme内容失败: {e}")
            return False
    
    
    async def _record_send_count(self):
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
                    "post_title": "模拟meme发送",
                    "send_success": True
                },
                query_type="create"
            )
        except Exception as e:
            print(f"记录发送次数失败: {e}")


class MemeStatusCommand(BaseCommand):
    """Meme发送状态查询命令"""
    
    command_name = "meme_status"
    command_description = "查看meme发送状态和统计信息"
    command_pattern = r"^/meme_status$"
    
    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        """执行状态查询"""
        try:
            # 检查是否启用插件
            if not self.get_config("plugin.enabled", False):
                await self.send_text("❌ Meme发送插件未启用")
                return True, "插件未启用", True
            
            # 获取今日发送次数
            today = datetime.now().strftime("%Y-%m-%d")
            today_count = await database_api.db_query(
                MemeSendRecords,
                query_type="count",
                filters={
                    "group_id": self.group_id,
                    "send_date": today
                }
            )
            
            # 获取配置信息
            max_daily = self.get_config("posting.max_daily_sends", 3)
            tieba_name = self.get_config("tieba.tieba_name", "搬石")
            
            # 构建状态消息
            status_message = f"""📊 **Meme发送状态报告**

🏷️ **群组**: {self.group_name}
📅 **日期**: {today}
📈 **今日发送**: {today_count}/{max_daily}
🎯 **目标贴吧**: {tieba_name}
⚙️ **插件状态**: {'✅ 启用' if self.get_config('plugin.enabled', False) else '❌ 禁用'}

💡 **使用说明**:
- 插件会随机发送贴吧meme内容
- 每日最多发送 {max_daily} 次
- 可通过配置文件调整参数"""
            
            await self.send_text(status_message)
            return True, f"显示了meme状态信息", True
            
        except Exception as e:
            await self.send_text(f"❌ 查询状态失败: {str(e)}")
            return False, f"查询失败: {str(e)}", True


@register_plugin
class MemePosterPlugin(BasePlugin):
    """贴吧Meme梗图自动发送插件"""
    
    # 插件基本信息
    plugin_name = "meme_poster_plugin"
    enable_plugin = True
    dependencies = []
    python_dependencies = ["aiohttp", "Pillow"]
    config_file_name = "config.toml"
    
    # 配置节描述
    config_section_descriptions = {
        "plugin": "插件基本配置",
        "posting": "发送控制配置", 
        "tieba": "贴吧数据源配置",
        "filtering": "内容过滤配置",
        "scheduling": "定时任务配置"
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
            "tieba_name": ConfigField(
                type=str, 
                default="搬石", 
                description="目标贴吧名称",
                example="沙雕图"
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
            "check_interval": ConfigField(
                type=int,
                default=300,
                description="检查间隔（秒）",
                example=600
            )
        }
    }
    
    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        """返回插件包含的组件列表"""
        return [
            (MemePosterAction.get_action_info(), MemePosterAction),
            (MemeStatusCommand.get_command_info(), MemeStatusCommand),
        ]
