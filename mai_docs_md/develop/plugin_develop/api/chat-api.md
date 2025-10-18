聊天API | MaiBot 文档中心



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

# 聊天API [​](#聊天api)

聊天API模块专门负责聊天信息的查询和管理，帮助插件获取和管理不同的聊天流。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system import chat_api
# 或者
from src.plugin_system.apis import chat_api
```

一种**Deprecated**方式：

python

```
from src.plugin_system.apis.chat_api import ChatManager
```

## 主要功能 [​](#主要功能)

### 1. 获取所有的聊天流 [​](#_1-获取所有的聊天流)

python

```
def get_all_streams(platform: Optional[str] | SpecialTypes = "qq") -> List[ChatStream]:
```

**Args**:

* `platform`：平台筛选，默认为"qq"，可以使用`SpecialTypes`枚举类中的`SpecialTypes.ALL_PLATFORMS`来获取所有平台的聊天流。

**Returns**:

* `List[ChatStream]`：聊天流列表

### 2. 获取群聊聊天流 [​](#_2-获取群聊聊天流)

python

```
def get_group_streams(platform: Optional[str] | SpecialTypes = "qq") -> List[ChatStream]:
```

**Args**:

* `platform`：平台筛选，默认为"qq"，可以使用`SpecialTypes`枚举类中的`SpecialTypes.ALL_PLATFORMS`来获取所有平台的群聊流。

**Returns**:

* `List[ChatStream]`：群聊聊天流列表

### 3. 获取私聊聊天流 [​](#_3-获取私聊聊天流)

python

```
def get_private_streams(platform: Optional[str] | SpecialTypes = "qq") -> List[ChatStream]:
```

**Args**:

* `platform`：平台筛选，默认为"qq"，可以使用`SpecialTypes`枚举类中的`SpecialTypes.ALL_PLATFORMS`来获取所有平台的私聊流。

**Returns**:

* `List[ChatStream]`：私聊聊天流列表

### 4. 根据群ID获取聊天流 [​](#_4-根据群id获取聊天流)

python

```
def get_stream_by_group_id(group_id: str, platform: Optional[str] | SpecialTypes = "qq") -> Optional[ChatStream]:
```

**Args**:

* `group_id`：群聊ID
* `platform`：平台筛选，默认为"qq"，可以使用`SpecialTypes`枚举类中的`SpecialTypes.ALL_PLATFORMS`来获取所有平台的群聊流。

**Returns**:

* `Optional[ChatStream]`：聊天流对象，如果未找到返回None

### 5. 根据用户ID获取私聊流 [​](#_5-根据用户id获取私聊流)

python

```
def get_stream_by_user_id(user_id: str, platform: Optional[str] | SpecialTypes = "qq") -> Optional[ChatStream]:
```

**Args**:

* `user_id`：用户ID
* `platform`：平台筛选，默认为"qq"，可以使用`SpecialTypes`枚举类中的`SpecialTypes.ALL_PLATFORMS`来获取所有平台的私聊流。

**Returns**:

* `Optional[ChatStream]`：聊天流对象，如果未找到返回None

### 6. 获取聊天流类型 [​](#_6-获取聊天流类型)

python

```
def get_stream_type(chat_stream: ChatStream) -> str:
```

**Args**:

* `chat_stream`：聊天流对象

**Returns**:

* `str`：聊天流类型，可能的值包括`private`（私聊流），`group`（群聊流）以及`unknown`（未知类型）。

### 7. 获取聊天流信息 [​](#_7-获取聊天流信息)

python

```
def get_stream_info(chat_stream: ChatStream) -> Dict[str, Any]:
```

**Args**:

* `chat_stream`：聊天流对象

**Returns**:

* `Dict[str, Any]`：聊天流的详细信息，包括但不限于：
  + `stream_id`：聊天流ID
  + `platform`：平台名称
  + `type`：聊天流类型
  + `group_id`：群聊ID
  + `group_name`：群聊名称
  + `user_id`：用户ID
  + `user_name`：用户名称

### 8. 获取聊天流统计摘要 [​](#_8-获取聊天流统计摘要)

python

```
def get_streams_summary() -> Dict[str, int]:
```

**Returns**:

* `Dict[str, int]`：聊天流统计信息摘要，包含以下键：
  + `total_streams`：总聊天流数量
  + `group_streams`：群聊流数量
  + `private_streams`：私聊流数量
  + `qq_streams`：QQ平台流数量

## 注意事项 [​](#注意事项)

1. 大部分函数在参数不合法时候会抛出异常，请确保你的程序进行了捕获。
2. `ChatStream`对象包含了聊天的完整信息，包括用户信息、群信息等。

最后更新:

Pager

[Previous page消息API](/develop/plugin_develop/api/message-api.md)

[Next pageLLM API](/develop/plugin_develop/api/llm-api.md)