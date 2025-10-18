# 贴吧Meme梗图自动发送插件

这是一个MaiBot插件，能够自动从百度贴吧获取meme梗图并发送到指定的QQ群组。

## 功能特性

- 🎯 **自动获取**: 从指定贴吧自动获取帖子内容
- 🔍 **智能识别**: 使用AI算法识别meme梗图内容
- ⏰ **定时发送**: 支持定时自动发送功能
- 📊 **次数限制**: 可配置每日最大发送次数
- 🎛️ **灵活配置**: 支持群组、关键词、时间等多维度配置
- 📈 **状态监控**: 提供发送状态查询命令

## 安装方法

1. 将插件文件夹 `meme_poster_plugin` 复制到MaiBot的插件目录
2. 确保安装了必要的Python依赖：
   ```bash
   pip install aiohttp Pillow numpy
   ```
3. 重启MaiBot，插件会自动加载

## 配置说明

插件启动后会自动生成 `config.toml` 配置文件，主要配置项如下：

### 基本配置
```toml
[plugin]
enabled = false  # 是否启用插件
config_version = "1.0.0"  # 配置文件版本
```

### 发送控制
```toml
[posting]
allowed_groups = []  # 允许发送的群组ID列表，为空表示所有群组
max_daily_sends = 3  # 每日最大发送次数
send_interval_min = 30  # 发送间隔（分钟）
```

### 贴吧配置
```toml
[tieba]
tieba_name = "搬石"  # 目标贴吧名称
fetch_count = 10  # 每次获取的帖子数量
use_mock = true  # 是否使用模拟数据（测试用）
api_url = ""  # 贴吧API地址（可选）
```

### 内容过滤
```toml
[filtering]
meme_keywords = ["梗图", "沙雕", "表情包", "meme", "搞笑", "沙雕图"]  # meme关键词
min_image_count = 1  # 帖子最少图片数量
```

### 定时任务
```toml
[scheduling]
enable_auto_send = true  # 是否启用自动发送
check_interval = 300  # 检查间隔（秒）
```

## 使用方法

### 1. 启用插件
编辑 `config.toml` 文件，将 `plugin.enabled` 设置为 `true`

### 2. 配置群组
在 `posting.allowed_groups` 中添加允许发送的群组ID

### 3. 调整参数
根据需要调整发送次数、间隔、关键词等参数

### 4. 查看状态
在群聊中发送 `/meme_status` 命令查看插件状态

## 命令说明

- `/meme_status` - 查看meme发送状态和统计信息

## 工作原理

1. **数据获取**: 插件定期从指定贴吧获取帖子列表
2. **内容筛选**: 使用关键词和AI算法筛选出meme内容
3. **智能发送**: 根据配置的规则自动发送到群组
4. **记录统计**: 记录发送历史，控制发送频率

## 技术特性

- **模块化设计**: 爬虫、检测器、数据库等模块独立
- **异步处理**: 使用asyncio实现高性能异步处理
- **错误处理**: 完善的异常处理和日志记录
- **可扩展性**: 支持自定义爬虫和检测算法

## 注意事项

1. **网络限制**: 贴吧可能有反爬虫机制，建议使用模拟数据测试
2. **发送频率**: 请合理设置发送频率，避免被群组管理员限制
3. **内容审核**: 插件会过滤内容，但仍需注意群组规则
4. **资源消耗**: 图片处理会消耗一定CPU和内存资源

## 开发说明

### 文件结构
```
meme_poster_plugin/
├── _manifest.json          # 插件清单
├── plugin.py              # 主插件文件
├── database_models.py     # 数据库模型
├── tieba_crawler.py       # 贴吧爬虫
├── meme_detector.py       # Meme检测器
└── README.md              # 说明文档
```

### 扩展开发
- 可以继承 `TiebaCrawler` 类实现自定义爬虫
- 可以继承 `MemeDetector` 类实现自定义检测算法
- 可以添加新的数据库模型来存储更多信息

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个插件！
