"""
Meme图片识别和检测模块
"""

import asyncio
import base64
import io
import json
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import aiohttp


class MemeDetector:
    """Meme图片检测器"""
    
    def __init__(self):
        self.meme_keywords = [
            "梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图",
            "沙雕", "搞笑图", "表情", "斗图", "搞笑表情"
        ]
        
        # 常见的meme特征
        self.meme_features = {
            'text_overlay': True,  # 是否有文字覆盖
            'bright_colors': True,  # 是否使用明亮颜色
            'simple_design': True,  # 设计是否简单
            'humorous_content': True  # 内容是否幽默
        }
    
    async def detect_meme(self, image_data: bytes, title: str = "", content: str = "") -> Tuple[bool, float, Dict]:
        """
        检测图片是否为meme
        
        Args:
            image_data: 图片二进制数据
            title: 帖子标题
            content: 帖子内容
            
        Returns:
            (是否为meme, 评分, 特征信息)
        """
        try:
            # 加载图片
            image = Image.open(io.BytesIO(image_data))
            
            # 提取图片特征
            features = await self._extract_image_features(image)
            
            # 提取文本特征
            text_features = self._extract_text_features(title, content)
            
            # 计算meme评分
            meme_score = self._calculate_meme_score(features, text_features)
            
            # 判断是否为meme（评分大于0.6认为是meme）
            is_meme = meme_score >= 0.6
            
            return is_meme, meme_score, {
                'image_features': features,
                'text_features': text_features,
                'meme_score': meme_score
            }
            
        except Exception as e:
            print(f"Meme检测失败: {e}")
            return False, 0.0, {}
    
    async def _extract_image_features(self, image: Image.Image) -> Dict:
        """提取图片特征"""
        features = {}
        
        try:
            # 转换为RGB模式
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 获取图片尺寸
            width, height = image.size
            features['aspect_ratio'] = width / height if height > 0 else 1.0
            features['size'] = (width, height)
            
            # 转换为numpy数组进行分析
            img_array = np.array(image)
            
            # 颜色分析
            features['color_variance'] = float(np.var(img_array))
            features['brightness'] = float(np.mean(img_array))
            
            # 边缘检测（简单版本）
            gray = np.mean(img_array, axis=2)
            edges = np.abs(np.diff(gray, axis=0)) + np.abs(np.diff(gray, axis=1))
            features['edge_density'] = float(np.mean(edges))
            
            # 文字检测（简单版本 - 检测高对比度区域）
            contrast = np.std(img_array, axis=2)
            features['text_likelihood'] = float(np.mean(contrast > np.mean(contrast) * 1.5))
            
            # 颜色分布
            features['color_diversity'] = len(np.unique(img_array.reshape(-1, 3), axis=0))
            
        except Exception as e:
            print(f"图片特征提取失败: {e}")
            features = {
                'aspect_ratio': 1.0,
                'size': (100, 100),
                'color_variance': 0.0,
                'brightness': 128.0,
                'edge_density': 0.0,
                'text_likelihood': 0.0,
                'color_diversity': 0
            }
        
        return features
    
    def _extract_text_features(self, title: str, content: str) -> Dict:
        """提取文本特征"""
        text = f"{title} {content}".lower()
        
        features = {
            'meme_keyword_count': 0,
            'text_length': len(text),
            'has_emoji': any(ord(char) > 127 for char in text),
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'laugh_patterns': 0
        }
        
        # 统计meme关键词
        for keyword in self.meme_keywords:
            if keyword.lower() in text:
                features['meme_keyword_count'] += 1
        
        # 检测笑声模式
        laugh_patterns = ['哈哈', 'haha', 'lol', '笑死', '233', '666']
        for pattern in laugh_patterns:
            features['laugh_patterns'] += text.count(pattern)
        
        return features
    
    def _calculate_meme_score(self, image_features: Dict, text_features: Dict) -> float:
        """计算meme评分"""
        score = 0.0
        
        # 文本特征评分（权重0.6）
        text_score = 0.0
        
        # 关键词评分
        keyword_score = min(text_features['meme_keyword_count'] * 0.2, 0.4)
        text_score += keyword_score
        
        # 感叹号评分（表示情绪）
        exclamation_score = min(text_features['exclamation_count'] * 0.05, 0.1)
        text_score += exclamation_score
        
        # 笑声模式评分
        laugh_score = min(text_features['laugh_patterns'] * 0.1, 0.2)
        text_score += laugh_score
        
        # 表情符号评分
        if text_features['has_emoji']:
            text_score += 0.1
        
        # 图片特征评分（权重0.4）
        image_score = 0.0
        
        # 文字覆盖可能性评分
        if image_features['text_likelihood'] > 0.3:
            image_score += 0.2
        
        # 颜色多样性评分
        if image_features['color_diversity'] > 50:
            image_score += 0.1
        
        # 边缘密度评分（meme通常有清晰的边缘）
        if image_features['edge_density'] > 10:
            image_score += 0.1
        
        # 计算总分
        total_score = text_score * 0.6 + image_score * 0.4
        
        return min(total_score, 1.0)
    
    async def create_mock_meme_image(self, title: str = "Meme图片") -> bytes:
        """创建模拟meme图片"""
        try:
            # 创建图片
            width, height = 400, 300
            image = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # 添加背景色
            bg_colors = [
                (255, 200, 200),  # 浅红色
                (200, 255, 200),  # 浅绿色
                (200, 200, 255),  # 浅蓝色
                (255, 255, 200),  # 浅黄色
            ]
            bg_color = bg_colors[hash(title) % len(bg_colors)]
            
            # 绘制渐变背景
            for y in range(height):
                color_ratio = y / height
                r = int(bg_color[0] * (1 - color_ratio) + 255 * color_ratio)
                g = int(bg_color[1] * (1 - color_ratio) + 255 * color_ratio)
                b = int(bg_color[2] * (1 - color_ratio) + 255 * color_ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # 添加文字
            try:
                # 尝试使用系统字体
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                # 使用默认字体
                font = ImageFont.load_default()
            
            # 计算文字位置
            text_bbox = draw.textbbox((0, 0), title, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # 绘制文字阴影
            draw.text((x + 2, y + 2), title, font=font, fill=(0, 0, 0))
            # 绘制文字
            draw.text((x, y), title, font=font, fill=(255, 0, 0))
            
            # 添加装饰边框
            draw.rectangle([5, 5, width-5, height-5], outline=(0, 0, 0), width=3)
            
            # 转换为字节
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            return buffer.getvalue()
            
        except Exception as e:
            print(f"创建模拟图片失败: {e}")
            # 返回一个简单的纯色图片
            image = Image.new('RGB', (400, 300), color=(255, 200, 200))
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            return buffer.getvalue()


class AdvancedMemeDetector(MemeDetector):
    """高级Meme检测器（使用AI模型）"""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    async def detect_meme_with_ai(self, image_data: bytes, title: str = "", content: str = "") -> Tuple[bool, float, str]:
        """
        使用AI模型检测meme
        
        Args:
            image_data: 图片二进制数据
            title: 帖子标题
            content: 帖子内容
            
        Returns:
            (是否为meme, 评分, 分析结果)
        """
        if not self.api_key:
            # 如果没有API密钥，回退到基础检测
            return await self.detect_meme(image_data, title, content)
        
        try:
            # 将图片转换为base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # 构建提示词
            prompt = f"""
            请分析以下内容是否为meme梗图：
            
            标题: {title}
            内容: {content}
            
            请从以下角度分析：
            1. 内容是否幽默搞笑
            2. 是否包含网络流行元素
            3. 是否适合作为表情包或梗图
            4. 是否符合meme的特征
            
            请返回JSON格式：
            {{
                "is_meme": true/false,
                "score": 0.0-1.0,
                "reason": "分析原因"
            }}
            """
            
            # 调用AI API
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-4-vision-preview',
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': prompt},
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:image/png;base64,{image_base64}'
                                }
                            }
                        ]
                    }
                ],
                'max_tokens': 500
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['choices'][0]['message']['content']
                        
                        # 解析JSON结果
                        try:
                            analysis = json.loads(content)
                            return (
                                analysis.get('is_meme', False),
                                analysis.get('score', 0.0),
                                analysis.get('reason', '')
                            )
                        except json.JSONDecodeError:
                            # 如果JSON解析失败，尝试从文本中提取信息
                            is_meme = 'true' in content.lower() or '是' in content
                            return is_meme, 0.5 if is_meme else 0.0, content
                    else:
                        print(f"AI API调用失败: {response.status}")
                        return await self.detect_meme(image_data, title, content)
                        
        except Exception as e:
            print(f"AI检测失败: {e}")
            return await self.detect_meme(image_data, title, content)
