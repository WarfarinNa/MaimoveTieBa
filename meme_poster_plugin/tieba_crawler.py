"""
百度贴吧数据爬取模块
"""

import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
import time
import random


class TiebaCrawler:
    """百度贴吧爬虫"""
    
    def __init__(self, session: aiohttp.ClientSession = None):
        self.session = session or aiohttp.ClientSession()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def fetch_tieba_posts(self, tieba_name: str, page: int = 1, count: int = 10) -> List[Dict]:
        """
        获取贴吧帖子列表
        
        Args:
            tieba_name: 贴吧名称
            page: 页码（从1开始）
            count: 获取数量
            
        Returns:
            帖子列表
        """
        try:
            # 构建贴吧URL
            base_url = f"https://tieba.baidu.com/f"
            params = {
                'kw': tieba_name,
                'pn': (page - 1) * 50,  # 每页50条
                'ie': 'utf-8'
            }
            
            async with self.session.get(base_url, params=params, headers=self.headers) as response:
                if response.status != 200:
                    print(f"请求失败: {response.status}")
                    return []
                
                html = await response.text()
                posts = self._parse_tieba_html(html)
                
                # 限制返回数量
                return posts[:count]
                
        except Exception as e:
            print(f"获取贴吧数据失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_tieba_html(self, html: str) -> List[Dict]:
        """解析贴吧HTML页面"""
        posts = []
        
        try:
            # 使用正则表达式提取帖子信息
            # 这里是一个简化的解析器，实际应该使用更robust的方法如BeautifulSoup
            
            # 匹配帖子标题和链接
            title_pattern = r'<a[^>]*class="j_th_tit"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
            title_matches = re.findall(title_pattern, html)
            
            # 匹配作者信息
            author_pattern = r'<span[^>]*class="tb_icon_author"[^>]*title="主题作者:([^"]*)"'
            author_matches = re.findall(author_pattern, html)
            
            # 匹配回复数和时间
            reply_pattern = r'<span[^>]*class="threadlist_rep_num"[^>]*>(\d+)</span>'
            reply_matches = re.findall(reply_pattern, html)
            
            # 组合数据
            for i, (url, title) in enumerate(title_matches):
                post = {
                    'title': title.strip(),
                    'url': urljoin('https://tieba.baidu.com', url),
                    'author': author_matches[i] if i < len(author_matches) else '未知',
                    'reply_count': int(reply_matches[i]) if i < len(reply_matches) else 0,
                    'images': [],  # 将在后续步骤中获取
                    'content': '',  # 将在后续步骤中获取
                    'post_time': '',  # 将在后续步骤中获取
                }
                posts.append(post)
                
        except Exception as e:
            print(f"解析HTML失败: {e}")
            import traceback
            traceback.print_exc()
        
        return posts
    
    async def fetch_post_detail(self, post_url: str) -> Dict:
        """
        获取帖子详细信息
        
        Args:
            post_url: 帖子URL
            
        Returns:
            帖子详细信息
        """
        try:
            async with self.session.get(post_url, headers=self.headers) as response:
                if response.status != 200:
                    return {}
                
                html = await response.text()
                return self._parse_post_detail(html)
                
        except Exception as e:
            print(f"获取帖子详情失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _parse_post_detail(self, html: str) -> Dict:
        """解析帖子详情页面"""
        detail = {
            'content': '',
            'images': [],
            'post_time': '',
            'floor_count': 0
        }
        
        try:
            # 提取帖子内容
            content_pattern = r'<div[^>]*class="d_post_content[^"]*"[^>]*>(.*?)</div>'
            content_matches = re.findall(content_pattern, html, re.DOTALL)
            if content_matches:
                # 清理HTML标签
                content = re.sub(r'<[^>]+>', '', content_matches[0])
                detail['content'] = content.strip()
            
            # 提取图片链接
            img_pattern = r'<img[^>]*class="BDE_Image"[^>]*src="([^"]*)"'
            img_matches = re.findall(img_pattern, html)
            detail['images'] = [url for url in img_matches if url.startswith('http')]
            
            # 提取发帖时间
            time_pattern = r'<span[^>]*class="tail-info"[^>]*>(\d{4}-\d{2}-\d{2} \d{2}:\d{2})</span>'
            time_matches = re.findall(time_pattern, html)
            if time_matches:
                detail['post_time'] = time_matches[0]
            
            # 提取楼层数
            floor_pattern = r'<span[^>]*class="red"[^>]*>(\d+)</span>'
            floor_matches = re.findall(floor_pattern, html)
            if floor_matches:
                detail['floor_count'] = int(floor_matches[0])
                
        except Exception as e:
            print(f"解析帖子详情失败: {e}")
            import traceback
            traceback.print_exc()
        
        return detail
    
    async def is_meme_content(self, post: Dict, keywords: List[str] = None) -> Tuple[bool, float]:
        """
        判断帖子是否为meme内容
        
        Args:
            post: 帖子信息
            keywords: meme关键词列表
            
        Returns:
            (是否为meme, 评分)
        """
        if keywords is None:
            keywords = ["梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图", "沙雕", "搞笑图"]
        
        title = post.get('title', '').lower()
        content = post.get('content', '').lower()
        
        # 关键词匹配
        keyword_score = 0
        for keyword in keywords:
            if keyword.lower() in title:
                keyword_score += 2  # 标题中的关键词权重更高
            if keyword.lower() in content:
                keyword_score += 1
        
        # 图片数量评分
        image_count = len(post.get('images', []))
        image_score = min(image_count * 0.5, 2)  # 最多2分
        
        # 回复数评分（热门帖子更可能是meme）
        reply_count = post.get('reply_count', 0)
        reply_score = min(reply_count * 0.01, 1)  # 最多1分
        
        # 总评分
        total_score = keyword_score + image_score + reply_score
        
        # 判断是否为meme（评分大于2认为是meme）
        is_meme = total_score >= 2
        
        return is_meme, total_score
    
    async def download_image(self, image_url: str) -> Optional[bytes]:
        """
        下载图片
        
        Args:
            image_url: 图片URL
            
        Returns:
            图片二进制数据
        """
        try:
            async with self.session.get(image_url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.read()
        except Exception as e:
            print(f"下载图片失败: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    async def close(self):
        """关闭会话"""
        if self.session and not self.session.closed:
            await self.session.close()


class MockTiebaCrawler:
    """模拟贴吧爬虫（用于测试）"""
    
    def __init__(self):
        self.mock_posts = [
            {
                'title': '【搬运】今日份的沙雕图合集',
                'content': '今天又收集了一些沙雕图，大家看看有没有喜欢的',
                'images': ['https://example.com/meme1.jpg', 'https://example.com/meme2.jpg'],
                'author': '搬运工小王',
                'post_time': '2024-01-01 12:00:00',
                'reply_count': 15,
                'url': 'https://tieba.baidu.com/p/1234567890'
            },
            {
                'title': '【梗图】这个表情包太真实了',
                'content': '看到这个表情包，我直接笑出声，太真实了',
                'images': ['https://example.com/meme3.jpg'],
                'author': '梗图收集者',
                'post_time': '2024-01-01 11:30:00',
                'reply_count': 8,
                'url': 'https://tieba.baidu.com/p/1234567891'
            },
            {
                'title': '【搞笑】沙雕网友的日常',
                'content': '沙雕网友的日常操作，笑死我了',
                'images': ['https://example.com/meme4.jpg', 'https://example.com/meme5.jpg'],
                'author': '沙雕观察员',
                'post_time': '2024-01-01 10:15:00',
                'reply_count': 23,
                'url': 'https://tieba.baidu.com/p/1234567892'
            },
            {
                'title': '【表情包】新的表情包出炉了',
                'content': '自己做的表情包，大家看看怎么样',
                'images': ['https://example.com/meme6.jpg'],
                'author': '表情包制作者',
                'post_time': '2024-01-01 09:45:00',
                'reply_count': 12,
                'url': 'https://tieba.baidu.com/p/1234567893'
            }
        ]
    
    async def fetch_tieba_posts(self, tieba_name: str, page: int = 1, count: int = 10) -> List[Dict]:
        """模拟获取贴吧帖子"""
        await asyncio.sleep(0.5)  # 模拟网络延迟
        return self.mock_posts[:count]
    
    async def fetch_post_detail(self, post_url: str) -> Dict:
        """模拟获取帖子详情"""
        await asyncio.sleep(0.3)
        return {
            'content': '这是帖子的详细内容...',
            'images': ['https://example.com/detail1.jpg'],
            'post_time': '2024-01-01 12:00:00',
            'floor_count': 1
        }
    
    async def is_meme_content(self, post: Dict, keywords: List[str] = None) -> Tuple[bool, float]:
        """模拟meme内容判断"""
        if keywords is None:
            keywords = ["梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图"]
        
        title = post.get('title', '').lower()
        content = post.get('content', '').lower()
        
        score = 0
        for keyword in keywords:
            if keyword.lower() in title:
                score += 2
            if keyword.lower() in content:
                score += 1
        
        # 图片数量加分
        score += len(post.get('images', [])) * 0.5
        
        is_meme = score >= 2
        return is_meme, score
    
    async def download_image(self, image_url: str) -> Optional[bytes]:
        """模拟下载图片"""
        await asyncio.sleep(0.2)
        # 返回一个简单的模拟图片数据
        return b'mock_image_data'
    
    async def close(self):
        """模拟关闭"""
        pass
