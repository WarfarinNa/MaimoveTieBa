插件管理API | MaiBot 文档中心



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

# 插件管理API [​](#插件管理api)

插件管理API模块提供了对插件的加载、卸载、重新加载以及目录管理功能。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import plugin_manage_api
# 或者
from src.plugin_system import plugin_manage_api
```

## 功能概述 [​](#功能概述)

插件管理API主要提供以下功能：

* **插件查询** - 列出当前加载的插件或已注册的插件。
* **插件管理** - 加载、卸载、重新加载插件。
* **插件目录管理** - 添加插件目录并重新扫描。

## 主要功能 [​](#主要功能)

### 1. 列出当前加载的插件 [​](#_1-列出当前加载的插件)

python

```
def list_loaded_plugins() -> List[str]:
```

列出所有当前加载的插件。

**Returns:**

* `List[str]` - 当前加载的插件名称列表。

### 2. 列出所有已注册的插件 [​](#_2-列出所有已注册的插件)

python

```
def list_registered_plugins() -> List[str]:
```

列出所有已注册的插件。

**Returns:**

* `List[str]` - 已注册的插件名称列表。

### 3. 获取插件路径 [​](#_3-获取插件路径)

python

```
def get_plugin_path(plugin_name: str) -> str:
```

获取指定插件的路径。

**Args:**

* `plugin_name` (str): 要查询的插件名称。 **Returns:**
* `str` - 插件的路径，如果插件不存在则 raise ValueError。

### 4. 卸载指定的插件 [​](#_4-卸载指定的插件)

python

```
async def remove_plugin(plugin_name: str) -> bool:
```

卸载指定的插件。

**Args:**

* `plugin_name` (str): 要卸载的插件名称。

**Returns:**

* `bool` - 卸载是否成功。

### 5. 重新加载指定的插件 [​](#_5-重新加载指定的插件)

python

```
async def reload_plugin(plugin_name: str) -> bool:
```

重新加载指定的插件。

**Args:**

* `plugin_name` (str): 要重新加载的插件名称。

**Returns:**

* `bool` - 重新加载是否成功。

### 6. 加载指定的插件 [​](#_6-加载指定的插件)

python

```
def load_plugin(plugin_name: str) -> Tuple[bool, int]:
```

加载指定的插件。

**Args:**

* `plugin_name` (str): 要加载的插件名称。

**Returns:**

* `Tuple[bool, int]` - 加载是否成功，成功或失败的个数。

### 7. 添加插件目录 [​](#_7-添加插件目录)

python

```
def add_plugin_directory(plugin_directory: str) -> bool:
```

添加插件目录。

**Args:**

* `plugin_directory` (str): 要添加的插件目录路径。

**Returns:**

* `bool` - 添加是否成功。

### 8. 重新扫描插件目录 [​](#_8-重新扫描插件目录)

python

```
def rescan_plugin_directory() -> Tuple[int, int]:
```

重新扫描插件目录，加载新插件。

**Returns:**

* `Tuple[int, int]` - 成功加载的插件数量和失败的插件数量。

最后更新:

Pager

[Previous page配置API](/develop/plugin_develop/api/config-api.md)

[Next page组件API](/develop/plugin_develop/api/component-manage-api.md)