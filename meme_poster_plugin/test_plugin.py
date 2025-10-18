"""
插件测试脚本
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meme_poster_plugin import MockTiebaCrawler, MemeDetector


async def test_tieba_crawler():
    """测试贴吧爬虫"""
    print("=== 测试贴吧爬虫 ===")
    
    crawler = MockTiebaCrawler()
    
    # 测试获取帖子
    posts = await crawler.fetch_tieba_posts("搬石", count=5)
    print(f"获取到 {len(posts)} 个帖子")
    
    for i, post in enumerate(posts):
        print(f"帖子 {i+1}: {post['title']}")
        print(f"  作者: {post['author']}")
        print(f"  回复数: {post['reply_count']}")
        print(f"  图片数: {len(post['images'])}")
        print()
    
    await crawler.close()


async def test_meme_detector():
    """测试meme检测器"""
    print("=== 测试Meme检测器 ===")
    
    detector = MemeDetector()
    
    # 测试文本特征提取
    title = "【搬运】今日份的沙雕图合集"
    content = "今天又收集了一些沙雕图，大家看看有没有喜欢的"
    
    text_features = detector._extract_text_features(title, content)
    print(f"文本特征: {text_features}")
    
    # 测试meme内容判断
    post = {
        'title': title,
        'content': content,
        'images': ['https://example.com/meme1.jpg'],
        'reply_count': 15
    }
    
    is_meme, score = await detector.is_meme_content(post)
    print(f"是否为meme: {is_meme}")
    print(f"评分: {score:.2f}")
    
    # 测试创建模拟图片
    print("创建模拟图片...")
    image_data = await detector.create_mock_meme_image("测试Meme")
    print(f"图片大小: {len(image_data)} 字节")


async def test_integration():
    """测试集成功能"""
    print("=== 测试集成功能 ===")
    
    # 模拟完整的meme检测流程
    crawler = MockTiebaCrawler()
    detector = MemeDetector()
    
    # 获取帖子
    posts = await crawler.fetch_tieba_posts("搬石", count=3)
    print(f"获取到 {len(posts)} 个帖子")
    
    # 检测meme内容
    meme_posts = []
    for post in posts:
        is_meme, score = await detector.is_meme_content(post)
        if is_meme:
            post['meme_score'] = score
            meme_posts.append(post)
            print(f"发现meme: {post['title']} (评分: {score:.2f})")
    
    print(f"筛选出 {len(meme_posts)} 个meme帖子")
    
    await crawler.close()


async def main():
    """主测试函数"""
    print("开始测试贴吧Meme插件...")
    print("=" * 50)
    
    try:
        await test_tieba_crawler()
        print()
        await test_meme_detector()
        print()
        await test_integration()
        
        print("=" * 50)
        print("所有测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
