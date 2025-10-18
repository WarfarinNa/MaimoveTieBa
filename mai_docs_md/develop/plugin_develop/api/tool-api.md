工具API | MaiBot 文档中心



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

# 工具API [​](#工具api)

工具API模块提供了获取和管理工具实例的功能，让插件能够访问系统中注册的工具。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import tool_api
# 或者
from src.plugin_system import tool_api
```

## 主要功能 [​](#主要功能)

### 1. 获取工具实例 [​](#_1-获取工具实例)

python

```
def get_tool_instance(tool_name: str) -> Optional[BaseTool]:
```

获取指定名称的工具实例。

**Args**:

* `tool_name`: 工具名称字符串

**Returns**:

* `Optional[BaseTool]`: 工具实例，如果工具不存在则返回 None

### 2. 获取LLM可用的工具定义 [​](#_2-获取llm可用的工具定义)

python

```
def get_llm_available_tool_definitions():
```

获取所有LLM可用的工具定义列表。

**Returns**:

* `List[Tuple[str, Dict[str, Any]]]`: 工具定义列表，每个元素为 `(工具名称, 工具定义字典)` 的元组
  + 其具体定义请参照[tool-components.md](./../tool-components.md)中的工具定义格式。

#### 示例： [​](#示例)

python

```
# 获取所有LLM可用的工具定义
tools = tool_api.get_llm_available_tool_definitions()
for tool_name, tool_definition in tools:
    print(f"工具: {tool_name}")
    print(f"定义: {tool_definition}")
```

## 注意事项 [​](#注意事项)

1. **工具存在性检查**：使用前请检查工具实例是否为 None
2. **权限控制**：某些工具可能有使用权限限制
3. **异步调用**：大多数工具方法是异步的，需要使用 await
4. **错误处理**：调用工具时请做好异常处理

最后更新:

Pager

[Previous page日志API](/develop/plugin_develop/api/logging-api.md)

[Next pageMaim\_Message 概述](/develop/maim_message/)