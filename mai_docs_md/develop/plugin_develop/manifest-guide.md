📄 插件Manifest系统指南 | MaiBot 文档中心



[Skip to content](#VPContent)

[MaiBot 文档中心](/)

Search`K`

 Main Navigation [首页](/)[用户手册](/manual/)[开发文档](/develop/)

官方Q群

[一群](https://qm.qq.com/q/VQ3XZrWgMs)

[二群](https://qm.qq.com/q/RzmCiRtHEW)

[三群](https://qm.qq.com/q/wlH5eT8OmQ)

[四群](https://qm.qq.com/q/fRdCbMXkGY)

[五群](https://qm.qq.com/q/JxvHZnxyec)

GitHub

[MaiBot](https://github.com/MaiM-with-u/MaiBot)

[MaiBot Docs](https://github.com/MaiM-with-u/docs)

Appearance

Menu

Return to top

 Sidebar Navigation 

## 开发文档

[介绍](/develop/)

[开发者与代码规范](/develop/develop_standard.html)

## 适配器开发

[开发综述](/develop/adapter_develop/)

[Adapter 开发指南](/develop/adapter_develop/develop_adapter.html)

## 插件开发

[开发指南](/develop/plugin_develop/)

[快速开始](/develop/plugin_develop/quick-start.md)

[Manifest系统指南](/develop/plugin_develop/manifest-guide.md)

[Actions系统](/develop/plugin_develop/action-components.md)

[命令处理系统](/develop/plugin_develop/command-components.md)

[工具系统](/develop/plugin_develop/tool-components.md)

[配置管理指南](/develop/plugin_develop/configuration-guide.md)

[依赖管理](/develop/plugin_develop/dependency-management.md)

### API参考

[发送API](/develop/plugin_develop/api/send-api.md)

[消息API](/develop/plugin_develop/api/message-api.md)

[聊天流API](/develop/plugin_develop/api/chat-api.md)

[LLM API](/develop/plugin_develop/api/llm-api.md)

[回复生成器API](/develop/plugin_develop/api/generator-api.md)

[表情包API](/develop/plugin_develop/api/emoji-api.md)

[人物信息API](/develop/plugin_develop/api/person-api.md)

[数据库API](/develop/plugin_develop/api/database-api.md)

[配置API](/develop/plugin_develop/api/config-api.md)

[插件API](/develop/plugin_develop/api/plugin-manage-api.md)

[组件API](/develop/plugin_develop/api/component-manage-api.md)

[日志API](/develop/plugin_develop/api/logging-api.md)

[工具API](/develop/plugin_develop/api/tool-api.md)

## Maim\_Message参考

[Maim\_Message 概述](/develop/maim_message/)

[Message\_Base](/develop/maim_message/message_base.html)

[Router](/develop/maim_message/router.html)

[命令参数表](/develop/maim_message/command_args.html)

On this page

# 📄 插件Manifest系统指南 [​](#📄-插件manifest系统指南)

## 概述 [​](#概述)

MaiBot插件系统现在强制要求每个插件都必须包含一个 `_manifest.json` 文件。这个文件描述了插件的基本信息、依赖关系、组件等重要元数据。

### 🔄 配置架构：Manifest与Config的职责分离 [​](#🔄-配置架构-manifest与config的职责分离)

为了避免信息重复和提高维护性，我们采用了**双文件架构**：

* **`_manifest.json`** - 插件的**静态元数据**

  + 插件身份信息（名称、版本、描述）
  + 开发者信息（作者、许可证、仓库）
  + 系统信息（兼容性、组件列表、分类）
* **`config.toml`** - 插件的**运行时配置**

  + 启用状态 (`enabled`)
  + 功能参数配置
  + 用户可调整的行为设置

这种分离确保了：

* ✅ 元数据信息统一管理
* ✅ 运行时配置灵活调整
* ✅ 避免重复维护
* ✅ 更清晰的职责划分

## 🔧 Manifest文件结构 [​](#🔧-manifest文件结构)

### 必需字段 [​](#必需字段)

以下字段是必需的，不能为空：

json

```
{
  "manifest_version": 1,
  "name": "插件显示名称",
  "version": "1.0.0",
  "description": "插件功能描述",
  "author": {
    "name": "作者名称"
  }
}
```

### 可选字段 [​](#可选字段)

以下字段都是可选的，可以根据需要添加：

json

```
{
  "license": "MIT",
  "host_application": {
    "min_version": "1.0.0",
    "max_version": "4.0.0"
  },
  "homepage_url": "https://github.com/your-repo",
  "repository_url": "https://github.com/your-repo",
  "keywords": ["关键词1", "关键词2"],
  "categories": ["分类1", "分类2"],
  "default_locale": "zh-CN",
  "locales_path": "_locales",
  "plugin_info": {
    "is_built_in": false,
    "plugin_type": "general",
    "components": [
      {
        "type": "action",
        "name": "组件名称",
        "description": "组件描述"
      }
    ]
  }
}
```

## 🛠️ 管理工具 [​](#🛠️-管理工具)

### 使用manifest\_tool.py [​](#使用manifest-tool-py)

我们提供了一个命令行工具来帮助管理manifest文件：

bash

```
# 扫描缺少manifest的插件
python scripts/manifest_tool.py scan src/plugins

# 为插件创建最小化manifest文件
python scripts/manifest_tool.py create-minimal src/plugins/my_plugin --name "我的插件" --author "作者"

# 为插件创建完整manifest模板
python scripts/manifest_tool.py create-complete src/plugins/my_plugin --name "我的插件"

# 验证manifest文件
python scripts/manifest_tool.py validate src/plugins/my_plugin
```

### 验证示例 [​](#验证示例)

验证通过的示例：

```
✅ Manifest文件验证通过
```

验证失败的示例：

```
❌ 验证错误:
  - 缺少必需字段: name
  - 作者信息缺少name字段或为空
⚠️ 验证警告:
  - 建议填写字段: license
  - 建议填写字段: keywords
```

## 🔄 迁移指南 [​](#🔄-迁移指南)

### 对于现有插件 [​](#对于现有插件)

1. **检查缺少manifest的插件**：

   bash

   ```
   python scripts/manifest_tool.py scan src/plugins
   ```
2. **为每个插件创建manifest**：

   bash

   ```
   python scripts/manifest_tool.py create-minimal src/plugins/your_plugin
   ```
3. **编辑manifest文件**，填写正确的信息。
4. **验证manifest**：

   bash

   ```
   python scripts/manifest_tool.py validate src/plugins/your_plugin
   ```

### 对于新插件 [​](#对于新插件)

创建新插件时，建议的步骤：

1. **创建插件目录和基本文件**
2. **创建完整manifest模板**：

   bash

   ```
   python scripts/manifest_tool.py create-complete src/plugins/new_plugin
   ```
3. **根据实际情况修改manifest文件**
4. **编写插件代码**
5. **验证manifest文件**

## 📋 字段说明 [​](#📋-字段说明)

### 基本信息 [​](#基本信息)

* `manifest_version`: manifest格式版本，当前为1
* `name`: 插件显示名称（必需）
* `version`: 插件版本号（必需）
* `description`: 插件功能描述（必需）
* `author`: 作者信息（必需）
  + `name`: 作者名称（必需）
  + `url`: 作者主页（可选）

### 许可和URL [​](#许可和url)

* `license`: 插件许可证（可选，建议填写）
* `homepage_url`: 插件主页（可选）
* `repository_url`: 源码仓库地址（可选）

### 分类和标签 [​](#分类和标签)

* `keywords`: 关键词数组（可选，建议填写）
* `categories`: 分类数组（可选，建议填写）

#### 🏷️ Categories分类系统说明 [​](#🏷️-categories分类系统说明)

插件系统使用预定义的分类系统来组织和管理插件。`categories` 字段必须使用以下**英文分类标识符**中的一个或多个：

| 英文分类标识符 | 中文显示名称 | 说明 |
| --- | --- | --- |
| `Group Management` | 群组管理 | 群组相关的管理功能插件 |
| `Entertainment & Interaction` | 娱乐互动 | 娱乐和互动类插件 |
| `Utility Tools` | 实用工具 | 实用工具类插件 |
| `Content Generation` | 内容生成 | 内容生成相关插件 |
| `Multimedia` | 多媒体 | 多媒体处理插件 |
| `External Integration` | 外部集成 | 外部服务集成插件 |
| `Data Analysis & Insights` | 数据分析与洞察 | 数据分析相关插件 |
| `Other` | 其他 | 其他未分类插件 |

**示例用法**：

json

```
{
  "categories": ["Entertainment & Interaction"],
  // 或者多个分类
  "categories": ["Utility Tools", "External Integration"]
}
```

⚠️ **重要提醒**：

* 必须使用表格中的**英文分类标识符**，否则插件无法被正确分类
* 如果不确定分类，建议使用 `Other`
* 系统会自动将英文分类映射为中文显示名称

### 兼容性 [​](#兼容性)

* `host_application`: 主机应用兼容性（必填）
  + `min_version`: 最低兼容版本（必填）
  + `max_version`: 最高兼容版本（可选，但建议填写，不填写默认到最新版本）

⚠️ 在不填写最高兼容版本的情况下，插件将默认支持从最低版本以上的所有版本。**（由于我们在不同版本对插件系统进行了大量的重构，这种情况几乎不可能。）**

### 国际化 [​](#国际化)

* `default_locale`: 默认语言（可选）
* `locales_path`: 语言文件目录（可选）

### 插件特定信息 [​](#插件特定信息)

* `plugin_info`: 插件详细信息（可选）
  + `is_built_in`: 是否为内置插件
  + `plugin_type`: 插件类型
  + `components`: 组件列表

## 示例文件 [​](#示例文件)

以下是一个遵循了上述良好实践的 `manifest.json` 文件范例。

json

```
{
  "manifest_version": 1, # 说明文件版本
  "name": "示例插件", # 插件名称
  "version": "1.0.0", # 插件版本
  "description": "这是一个示例插件", # 插件介绍
  "author": { # 插件作者信息
    "name": "MaiBot 团队", # 插件作者名称
    "url": "https://github.com/MaiM-with-u", # 插件作者主页
  },
  "license": "MIT", # 插件许可版本

  "host_application": {
    "min_version": "0.7.0", # 插件适配麦麦最低版本
    "max_version": "0.8.0" # （可选）插件适配麦麦最高版本
  },
  "homepage_url": "https://github.com/MaiM-with-u", # （可选）插件主页
  "repository_url": "https://github.com/MaiM-with-u/plugin-repo", # （可选）插件仓库地址
  "keywords": ["Example"], # 插件关键词
  "categories": ["Other"], # 插件分类
  
  "default_locale": "CN", # 插件默认语言
  "locales_path": "_locales" # （可选）插件语言文件夹
}
```

## ⚠️ 注意事项 [​](#⚠️-注意事项)

1. **强制要求**：所有插件必须包含`_manifest.json`文件，否则无法加载
2. **编码格式**：manifest文件必须使用UTF-8编码
3. **JSON格式**：文件必须是有效的JSON格式
4. **必需字段**：`manifest_version`、`name`、`version`、`description`、`author.name`是必需的
5. **版本兼容**：当前只支持`manifest_version = 1`

## 🔍 常见问题 [​](#🔍-常见问题)

### Q: 可以不填写可选字段吗？ [​](#q-可以不填写可选字段吗)

A: 可以。所有标记为"可选"的字段都可以不填写，但建议至少填写`license`和`keywords`。

### Q: manifest验证失败怎么办？ [​](#q-manifest验证失败怎么办)

A: 根据验证器的错误提示修复相应问题。错误会导致插件加载失败，警告不会。

## 📚 参考示例 [​](#📚-参考示例)

查看内置插件的manifest文件作为参考：

* `src/plugins/built_in/core_actions/_manifest.json`
* `src/plugins/built_in/tts_plugin/_manifest.json`
* `src/plugins/hello_world_plugin/_manifest.json`

最后更新:

Pager

[Previous page快速开始](/develop/plugin_develop/quick-start.md)

[Next pageActions系统](/develop/plugin_develop/action-components.md)