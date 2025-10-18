组件管理API | MaiBot 文档中心



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

# 组件管理API [​](#组件管理api)

组件管理API模块提供了对插件组件的查询和管理功能，使得插件能够获取和使用组件相关的信息。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import component_manage_api
# 或者
from src.plugin_system import component_manage_api
```

## 功能概述 [​](#功能概述)

组件管理API主要提供以下功能：

* **插件信息查询** - 获取所有插件或指定插件的信息。
* **组件查询** - 按名称或类型查询组件信息。
* **组件管理** - 启用或禁用组件，支持全局和局部操作。

## 主要功能 [​](#主要功能)

### 1. 获取所有插件信息 [​](#_1-获取所有插件信息)

python

```
def get_all_plugin_info() -> Dict[str, PluginInfo]:
```

获取所有插件的信息。

**Returns:**

* `Dict[str, PluginInfo]` - 包含所有插件信息的字典，键为插件名称，值为 `PluginInfo` 对象。

### 2. 获取指定插件信息 [​](#_2-获取指定插件信息)

python

```
def get_plugin_info(plugin_name: str) -> Optional[PluginInfo]:
```

获取指定插件的信息。

**Args:**

* `plugin_name` (str): 插件名称。

**Returns:**

* `Optional[PluginInfo]`: 插件信息对象，如果插件不存在则返回 `None`。

### 3. 获取指定组件信息 [​](#_3-获取指定组件信息)

python

```
def get_component_info(component_name: str, component_type: ComponentType) -> Optional[Union[CommandInfo, ActionInfo, EventHandlerInfo]]:
```

获取指定组件的信息。

**Args:**

* `component_name` (str): 组件名称。
* `component_type` (ComponentType): 组件类型。

**Returns:**

* `Optional[Union[CommandInfo, ActionInfo, EventHandlerInfo]]`: 组件信息对象，如果组件不存在则返回 `None`。

### 4. 获取指定类型的所有组件信息 [​](#_4-获取指定类型的所有组件信息)

python

```
def get_components_info_by_type(component_type: ComponentType) -> Dict[str, Union[CommandInfo, ActionInfo, EventHandlerInfo]]:
```

获取指定类型的所有组件信息。

**Args:**

* `component_type` (ComponentType): 组件类型。

**Returns:**

* `Dict[str, Union[CommandInfo, ActionInfo, EventHandlerInfo]]`: 包含指定类型组件信息的字典，键为组件名称，值为对应的组件信息对象。

### 5. 获取指定类型的所有启用的组件信息 [​](#_5-获取指定类型的所有启用的组件信息)

python

```
def get_enabled_components_info_by_type(component_type: ComponentType) -> Dict[str, Union[CommandInfo, ActionInfo, EventHandlerInfo]]:
```

获取指定类型的所有启用的组件信息。

**Args:**

* `component_type` (ComponentType): 组件类型。

**Returns:**

* `Dict[str, Union[CommandInfo, ActionInfo, EventHandlerInfo]]`: 包含指定类型启用组件信息的字典，键为组件名称，值为对应的组件信息对象。

### 6. 获取指定 Action 的注册信息 [​](#_6-获取指定-action-的注册信息)

python

```
def get_registered_action_info(action_name: str) -> Optional[ActionInfo]:
```

获取指定 Action 的注册信息。

**Args:**

* `action_name` (str): Action 名称。

**Returns:**

* `Optional[ActionInfo]` - Action 信息对象，如果 Action 不存在则返回 `None`。

### 7. 获取指定 Command 的注册信息 [​](#_7-获取指定-command-的注册信息)

python

```
def get_registered_command_info(command_name: str) -> Optional[CommandInfo]:
```

获取指定 Command 的注册信息。

**Args:**

* `command_name` (str): Command 名称。

**Returns:**

* `Optional[CommandInfo]` - Command 信息对象，如果 Command 不存在则返回 `None`。

### 8. 获取指定 Tool 的注册信息 [​](#_8-获取指定-tool-的注册信息)

python

```
def get_registered_tool_info(tool_name: str) -> Optional[ToolInfo]:
```

获取指定 Tool 的注册信息。

**Args:**

* `tool_name` (str): Tool 名称。

**Returns:**

* `Optional[ToolInfo]` - Tool 信息对象，如果 Tool 不存在则返回 `None`。

### 9. 获取指定 EventHandler 的注册信息 [​](#_9-获取指定-eventhandler-的注册信息)

python

```
def get_registered_event_handler_info(event_handler_name: str) -> Optional[EventHandlerInfo]:
```

获取指定 EventHandler 的注册信息。

**Args:**

* `event_handler_name` (str): EventHandler 名称。

**Returns:**

* `Optional[EventHandlerInfo]` - EventHandler 信息对象，如果 EventHandler 不存在则返回 `None`。

### 10. 全局启用指定组件 [​](#_10-全局启用指定组件)

python

```
def globally_enable_component(component_name: str, component_type: ComponentType) -> bool:
```

全局启用指定组件。

**Args:**

* `component_name` (str): 组件名称。
* `component_type` (ComponentType): 组件类型。

**Returns:**

* `bool` - 启用成功返回 `True`，否则返回 `False`。

### 11. 全局禁用指定组件 [​](#_11-全局禁用指定组件)

python

```
async def globally_disable_component(component_name: str, component_type: ComponentType) -> bool:
```

全局禁用指定组件。

**此函数是异步的，确保在异步环境中调用。**

**Args:**

* `component_name` (str): 组件名称。
* `component_type` (ComponentType): 组件类型。

**Returns:**

* `bool` - 禁用成功返回 `True`，否则返回 `False`。

### 12. 局部启用指定组件 [​](#_12-局部启用指定组件)

python

```
def locally_enable_component(component_name: str, component_type: ComponentType, stream_id: str) -> bool:
```

局部启用指定组件。

**Args:**

* `component_name` (str): 组件名称。
* `component_type` (ComponentType): 组件类型。
* `stream_id` (str): 消息流 ID。

**Returns:**

* `bool` - 启用成功返回 `True`，否则返回 `False`。

### 13. 局部禁用指定组件 [​](#_13-局部禁用指定组件)

python

```
def locally_disable_component(component_name: str, component_type: ComponentType, stream_id: str) -> bool:
```

局部禁用指定组件。

**Args:**

* `component_name` (str): 组件名称。
* `component_type` (ComponentType): 组件类型。
* `stream_id` (str): 消息流 ID。

**Returns:**

* `bool` - 禁用成功返回 `True`，否则返回 `False`。

### 14. 获取指定消息流中禁用的组件列表 [​](#_14-获取指定消息流中禁用的组件列表)

python

```
def get_locally_disabled_components(stream_id: str, component_type: ComponentType) -> list[str]:
```

获取指定消息流中禁用的组件列表。

**Args:**

* `stream_id` (str): 消息流 ID。
* `component_type` (ComponentType): 组件类型。

**Returns:**

* `list[str]` - 禁用的组件名称列表。

最后更新:

Pager

[Previous page插件API](/develop/plugin_develop/api/plugin-manage-api.md)

[Next page日志API](/develop/plugin_develop/api/logging-api.md)