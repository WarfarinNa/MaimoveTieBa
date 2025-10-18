个人信息API | MaiBot 文档中心



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

# 个人信息API [​](#个人信息api)

个人信息API模块提供用户信息查询和管理功能，让插件能够获取和使用用户的相关信息。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import person_api
# 或者
from src.plugin_system import person_api
```

## 主要功能 [​](#主要功能)

### 1. Person ID 获取 [​](#_1-person-id-获取)

python

```
def get_person_id(platform: str, user_id: int) -> str:
```

根据平台和用户ID获取person\_id

**Args:**

* `platform`：平台名称，如 "qq", "telegram" 等
* `user_id`：用户ID

**Returns:**

* `str`：唯一的person\_id（MD5哈希值）

#### 示例 [​](#示例)

python

```
person_id = person_api.get_person_id("qq", 123456)
```

### 2. 用户信息查询 [​](#_2-用户信息查询)

python

```
async def get_person_value(person_id: str, field_name: str, default: Any = None) -> Any:
```

查询单个用户信息字段值

**Args:**

* `person_id`：用户的唯一标识ID
* `field_name`：要获取的字段名
* `default`：字段值不存在时的默认值

**Returns:**

* `Any`：字段值或默认值

#### 示例 [​](#示例-1)

python

```
nickname = await person_api.get_person_value(person_id, "nickname", "未知用户")
impression = await person_api.get_person_value(person_id, "impression")
```

### 3. 批量用户信息查询 [​](#_3-批量用户信息查询)

python

```
async def get_person_values(person_id: str, field_names: list, default_dict: Optional[dict] = None) -> dict:
```

批量获取用户信息字段值

**Args:**

* `person_id`：用户的唯一标识ID
* `field_names`：要获取的字段名列表
* `default_dict`：默认值字典，键为字段名，值为默认值

**Returns:**

* `dict`：字段名到值的映射字典

#### 示例 [​](#示例-2)

python

```
values = await person_api.get_person_values(
    person_id,
    ["nickname", "impression", "know_times"],
    {"nickname": "未知用户", "know_times": 0}
)
```

### 4. 判断用户是否已知 [​](#_4-判断用户是否已知)

python

```
async def is_person_known(platform: str, user_id: int) -> bool:
```

判断是否认识某个用户

**Args:**

* `platform`：平台名称
* `user_id`：用户ID

**Returns:**

* `bool`：是否认识该用户

### 5. 根据用户名获取Person ID [​](#_5-根据用户名获取person-id)

python

```
def get_person_id_by_name(person_name: str) -> str:
```

根据用户名获取person\_id

**Args:**

* `person_name`：用户名

**Returns:**

* `str`：person\_id，如果未找到返回空字符串

## 常用字段说明 [​](#常用字段说明)

### 基础信息字段 [​](#基础信息字段)

* `nickname`：用户昵称
* `platform`：平台信息
* `user_id`：用户ID

### 关系信息字段 [​](#关系信息字段)

* `impression`：对用户的印象
* `points`: 用户特征点

其他字段可以参考`PersonInfo`类的属性（位于`src.common.database.database_model`）

## 注意事项 [​](#注意事项)

1. **异步操作**：部分查询函数都是异步的，需要使用`await`
2. **性能考虑**：批量查询优于单个查询
3. **隐私保护**：确保用户信息的使用符合隐私政策
4. **数据一致性**：person\_id是用户的唯一标识，应妥善保存和使用

最后更新:

Pager

[Previous page表情包API](/develop/plugin_develop/api/emoji-api.md)

[Next page数据库API](/develop/plugin_develop/api/database-api.md)