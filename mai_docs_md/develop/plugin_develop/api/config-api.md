配置API | MaiBot 文档中心



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

# 配置API [​](#配置api)

配置API模块提供了配置读取功能，让插件能够安全地访问全局配置和插件配置。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import config_api
# 或者
from src.plugin_system import config_api
```

## 主要功能 [​](#主要功能)

### 1. 访问全局配置 [​](#_1-访问全局配置)

python

```
def get_global_config(key: str, default: Any = None) -> Any:
```

**Args**:

* `key`: 命名空间式配置键名，使用嵌套访问，如 "section.subsection.key"，大小写敏感
* `default`: 如果配置不存在时返回的默认值

**Returns**:

* `Any`: 配置值或默认值

#### 示例： [​](#示例)

获取机器人昵称

python

```
bot_name = config_api.get_global_config("bot.nickname", "MaiBot")
```

### 2. 获取插件配置 [​](#_2-获取插件配置)

python

```
def get_plugin_config(plugin_config: dict, key: str, default: Any = None) -> Any:
```

**Args**:

* `plugin_config`: 插件配置字典
* `key`: 配置键名，支持嵌套访问如 "section.subsection.key"，大小写敏感
* `default`: 如果配置不存在时返回的默认值

**Returns**:

* `Any`: 配置值或默认值

## 注意事项 [​](#注意事项)

1. **只读访问**：配置API只提供读取功能，插件不能修改全局配置
2. **错误处理**：所有函数都有错误处理，失败时会记录日志并返回默认值
3. **安全性**：插件通过此API访问配置是安全和隔离的
4. **性能**：频繁访问的配置建议在插件初始化时获取并缓存

最后更新:

Pager

[Previous page数据库API](/develop/plugin_develop/api/database-api.md)

[Next page插件API](/develop/plugin_develop/api/plugin-manage-api.md)