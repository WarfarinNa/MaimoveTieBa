# 智能贴吧内容推送系统

## 📖 概述

这是一个智能的贴吧内容推送插件，能够自动获取指定贴吧的内容，利用LLM进行智能评价，并根据内容类型进行个性化推送。支持多群组、多贴吧、随机时间推送等功能。

## ✨ 主要功能

### 🧠 智能内容评价
- 使用LLM对贴吧内容进行智能评价
- 自动识别内容类型（meme梗图/二次元作品/信息分享/其他）
- 基于兴趣评分进行内容筛选
- 支持回退到基础关键词过滤

### 🎯 多贴吧支持
- 支持配置多个目标贴吧
- 随机选择贴吧进行内容获取
- 可指定特定贴吧进行推送

### ⏰ 智能时间推送
- 支持配置多个推送时间点
- 随机概率推送，符合人类作息
- 避免固定时间推送的机械感

### 🎨 内容类型识别
- **Meme梗图**: 直接推送图片，简洁描述
- **二次元作品**: 推送图片，使用画师相关描述
- **信息分享**: 使用LLM生成详细描述
- **其他内容**: 根据LLM评价结果处理

### 🔧 多参数配置
- 群组白名单管理
- 每日发送次数限制
- 推送时间点配置
- 推送概率调整
- LLM评价开关

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install aiohttp Pillow numpy
```

### 2. 配置插件
编辑生成的 `config.toml` 文件：

```toml
[plugin]
enabled = true

[tieba]
tieba_list = ["搬石", "沙雕图", "二次元", "技术"]
fetch_count = 10
use_mock = false

[posting]
allowed_groups = ["123456789", "987654321"]
max_daily_sends = 5

[scheduling]
push_hours = [9, 12, 15, 18, 21]
push_probability = 0.3

[llm]
enable_llm_evaluation = true
min_interest_score = 0.6
```

### 3. 使用命令
- `/tieba_status` - 查看推送状态
- `/tieba_config list` - 查看当前配置
- `/tieba_config help` - 查看配置帮助

## 📋 配置说明

### 基本配置
- `plugin.enabled`: 是否启用插件
- `plugin.config_version`: 配置文件版本

### 贴吧配置
- `tieba.tieba_list`: 目标贴吧列表
- `tieba.fetch_count`: 每次获取的帖子数量
- `tieba.use_mock`: 是否使用模拟数据（测试用）

### 推送配置
- `posting.allowed_groups`: 允许推送的群组ID列表
- `posting.max_daily_sends`: 每日最大发送次数
- `posting.send_interval_min`: 发送间隔（分钟）

### 时间配置
- `scheduling.push_hours`: 推送时间点（24小时制）
- `scheduling.push_probability`: 推送概率（0-1）
- `scheduling.check_interval`: 检查间隔（秒）

### LLM配置
- `llm.enable_llm_evaluation`: 是否启用LLM评价
- `llm.evaluation_model`: 评价使用的模型名称
- `llm.min_interest_score`: 最低兴趣评分阈值

## 🔄 工作流程

1. **时间检查**: 检查当前时间是否在推送时间范围内
2. **随机选择**: 随机选择目标贴吧
3. **内容获取**: 从贴吧获取指定数量的帖子
4. **LLM评价**: 使用LLM对每个帖子进行评价
5. **内容筛选**: 根据评价结果筛选符合要求的内容
6. **类型识别**: 识别内容类型并选择推送方式
7. **内容推送**: 根据类型推送内容到群组
8. **记录统计**: 记录推送统计信息

## 🛠️ 技术特性

### 异常处理
- 完善的异常处理机制
- 详细的错误日志记录
- 优雅的错误恢复

### 性能优化
- 异步处理提高效率
- 智能缓存减少重复请求
- 回退机制保证可用性

### 扩展性
- 模块化设计便于扩展
- 支持自定义内容类型
- 可配置的评价标准

## 📊 监控和统计

### 状态查询
使用 `/tieba_status` 命令可以查看：
- 当前群组推送状态
- 今日发送次数统计
- 配置信息概览
- 推送时间设置

### 配置管理
使用 `/tieba_config` 命令可以：
- 查看当前配置
- 获取配置帮助
- 了解配置项说明

## 🔧 开发说明

### 文件结构
```
meme_poster_plugin/
├── plugin.py              # 主插件文件
├── tieba_crawler.py       # 贴吧爬虫模块
├── meme_detector.py       # 内容检测模块
├── database_models.py     # 数据库模型
├── _manifest.json         # 插件清单
├── requirements.txt       # 依赖列表
└── README.md             # 说明文档
```

### 主要类
- `TiebaContentAction`: 智能内容推送Action
- `TiebaStatusCommand`: 状态查询Command
- `TiebaConfigCommand`: 配置管理Command
- `TiebaContentPlugin`: 主插件类

## 🐛 故障排除

### 常见问题
1. **LLM评价失败**: 检查LLM API配置和网络连接
2. **贴吧数据获取失败**: 检查网络连接和贴吧名称
3. **推送时间不准确**: 检查系统时区和时间配置
4. **配置不生效**: 确认配置文件格式正确并重启插件

### 调试建议
1. 启用详细日志记录
2. 使用模拟数据模式测试
3. 逐步验证各个功能模块
4. 检查依赖包版本兼容性

## 📝 更新日志

### v2.0.0
- 重构为智能贴吧内容推送系统
- 添加LLM评价功能
- 支持多贴吧配置
- 实现随机时间推送
- 添加内容类型识别
- 完善配置管理系统

### v1.0.0
- 基础meme梗图推送功能
- 简单的关键词过滤
- 基本配置管理

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个插件！

---

**注意**: 本插件需要MaiBot框架支持，请确保在正确的环境中使用。