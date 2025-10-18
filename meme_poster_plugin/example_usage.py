"""
插件使用示例
"""

import asyncio
from meme_poster_plugin import MemePosterAction, MemeDetector, MockTiebaCrawler


async def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建meme检测器
    detector = MemeDetector()
    
    # 创建模拟爬虫
    crawler = MockTiebaCrawler()
    
    # 获取贴吧帖子
    posts = await crawler.fetch_tieba_posts("搬石", count=5)
    print(f"从贴吧获取到 {len(posts)} 个帖子")
    
    # 筛选meme内容
    meme_posts = []
    for post in posts:
        is_meme, score = await detector.is_meme_content(post)
        if is_meme:
            post['meme_score'] = score
            meme_posts.append(post)
            print(f"✓ 发现meme: {post['title']} (评分: {score:.2f})")
        else:
            print(f"✗ 非meme: {post['title']} (评分: {score:.2f})")
    
    print(f"\n筛选出 {len(meme_posts)} 个meme帖子")
    
    # 创建模拟图片
    if meme_posts:
        best_meme = max(meme_posts, key=lambda x: x['meme_score'])
        print(f"\n最佳meme: {best_meme['title']}")
        
        # 生成模拟图片
        image_data = await detector.create_mock_meme_image(best_meme['title'])
        print(f"生成了 {len(image_data)} 字节的图片数据")
    
    await crawler.close()


async def example_advanced_detection():
    """高级检测示例"""
    print("\n=== 高级检测示例 ===")
    
    detector = MemeDetector()
    
    # 测试不同类型的帖子
    test_posts = [
        {
            'title': '【搬运】今日份的沙雕图合集',
            'content': '今天又收集了一些沙雕图，大家看看有没有喜欢的',
            'images': ['https://example.com/meme1.jpg'],
            'reply_count': 15
        },
        {
            'title': '【求助】电脑蓝屏了怎么办',
            'content': '我的电脑突然蓝屏了，有谁知道怎么解决吗？',
            'images': [],
            'reply_count': 3
        },
        {
            'title': '【表情包】新的表情包出炉了',
            'content': '自己做的表情包，大家看看怎么样！',
            'images': ['https://example.com/emoji1.jpg'],
            'reply_count': 8
        }
    ]
    
    for i, post in enumerate(test_posts, 1):
        print(f"\n测试帖子 {i}: {post['title']}")
        
        # 检测是否为meme
        is_meme, score = await detector.is_meme_content(post)
        
        print(f"  是否为meme: {'是' if is_meme else '否'}")
        print(f"  评分: {score:.2f}")
        print(f"  图片数量: {len(post['images'])}")
        print(f"  回复数量: {post['reply_count']}")


async def example_configuration():
    """配置示例"""
    print("\n=== 配置示例 ===")
    
    # 模拟配置
    config = {
        'tieba_name': '搬石',
        'max_daily_sends': 5,
        'meme_keywords': ['梗图', '沙雕', '表情包', 'meme', '搞笑'],
        'use_mock': True
    }
    
    print("推荐配置:")
    print(f"  目标贴吧: {config['tieba_name']}")
    print(f"  每日最大发送: {config['max_daily_sends']} 次")
    print(f"  Meme关键词: {', '.join(config['meme_keywords'])}")
    print(f"  使用模拟数据: {'是' if config['use_mock'] else '否'}")
    
    print("\n配置建议:")
    print("1. 首次使用建议开启模拟数据模式")
    print("2. 根据群组活跃度调整发送频率")
    print("3. 可以根据群组特点调整关键词列表")
    print("4. 建议设置合理的每日发送次数限制")


async def main():
    """主函数"""
    print("贴吧Meme插件使用示例")
    print("=" * 50)
    
    try:
        await example_basic_usage()
        await example_advanced_detection()
        await example_configuration()
        
        print("\n" + "=" * 50)
        print("示例运行完成！")
        print("\n使用说明:")
        print("1. 将插件文件夹复制到MaiBot的插件目录")
        print("2. 编辑 config.toml 配置文件")
        print("3. 重启MaiBot启用插件")
        print("4. 在群聊中发送 /meme_status 查看状态")
        
    except Exception as e:
        print(f"运行示例时出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
