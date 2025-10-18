表情包API | MaiBot 文档中心



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

# 表情包API [​](#表情包api)

表情包API模块提供表情包的获取、查询和管理功能，让插件能够智能地选择和使用表情包。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import emoji_api
# 或者
from src.plugin_system import emoji_api
```

## 二步走识别优化 [​](#二步走识别优化)

从新版本开始，表情包识别系统采用了**二步走识别 + 智能缓存**的优化方案：

### **收到表情包时的识别流程** [​](#收到表情包时的识别流程)

1. **第一步**：VLM视觉分析 - 生成详细描述
2. **第二步**：LLM情感分析 - 基于详细描述提取核心情感标签
3. **缓存机制**：将情感标签缓存到数据库，详细描述保存到Images表

### **注册表情包时的优化** [​](#注册表情包时的优化)

* **智能复用**：优先从Images表获取已有的详细描述
* **避免重复**：如果表情包之前被收到过，跳过VLM调用
* **性能提升**：减少不必要的AI调用，降低延时和成本

### **缓存策略** [​](#缓存策略)

* **ImageDescriptions表**：缓存最终的情感标签（用于快速显示）
* **Images表**：保存详细描述（用于注册时复用）
* **双重检查**：防止并发情况下的重复生成

## 主要功能 [​](#主要功能)

### 1. 表情包获取 [​](#_1-表情包获取)

python

```
async def get_by_description(description: str) -> Optional[Tuple[str, str, str]]:
```

根据场景描述选择表情包

**Args：**

* `description`：表情包的描述文本，例如"开心"、"难过"、"愤怒"等

**Returns：**

* `Optional[Tuple[str, str, str]]`：一个元组: (表情包的base64编码, 描述, 情感标签)，如果未找到匹配的表情包则返回None

#### 示例 [​](#示例)

python

```
emoji_result = await emoji_api.get_by_description("大笑")
if emoji_result:
    emoji_base64, description, matched_scene = emoji_result
    print(f"获取到表情包: {description}, 场景: {matched_scene}")
    # 可以将emoji_base64用于发送表情包
```

### 2. 随机获取表情包 [​](#_2-随机获取表情包)

python

```
async def get_random(count: Optional[int] = 1) -> List[Tuple[str, str, str]]:
```

随机获取指定数量的表情包

**Args：**

* `count`：要获取的表情包数量，默认为1

**Returns：**

* `List[Tuple[str, str, str]]`：一个包含多个表情包的列表，每个元素是一个元组: (表情包的base64编码, 描述, 情感标签)，如果未找到或出错则返回空列表

### 3. 根据情感获取表情包 [​](#_3-根据情感获取表情包)

python

```
async def get_by_emotion(emotion: str) -> Optional[Tuple[str, str, str]]:
```

根据情感标签获取表情包

**Args：**

* `emotion`：情感标签，例如"开心"、"悲伤"、"愤怒"等

**Returns：**

* `Optional[Tuple[str, str, str]]`：一个元组: (表情包的base64编码, 描述, 情感标签)，如果未找到则返回None

### 4. 获取表情包数量 [​](#_4-获取表情包数量)

python

```
def get_count() -> int:
```

获取当前可用表情包的数量

### 5. 获取表情包系统信息 [​](#_5-获取表情包系统信息)

python

```
def get_info() -> Dict[str, Any]:
```

获取表情包系统的基本信息

**Returns：**

* `Dict[str, Any]`：包含表情包数量、描述等信息的字典，包含以下键：
  + `current_count`：当前表情包数量
  + `max_count`：最大表情包数量
  + `available_emojis`：当前可用的表情包数量

### 6. 获取所有可用的情感标签 [​](#_6-获取所有可用的情感标签)

python

```
def get_emotions() -> List[str]:
```

获取所有可用的情感标签 **（已经去重）**

### 7. 获取所有表情包描述 [​](#_7-获取所有表情包描述)

python

```
def get_descriptions() -> List[str]:
```

获取所有表情包的描述列表

## 场景描述说明 [​](#场景描述说明)

### 常用场景描述 [​](#常用场景描述)

表情包系统支持多种具体的场景描述，举例如下：

* **开心类场景**：开心的大笑、满意的微笑、兴奋的手舞足蹈
* **无奈类场景**：表示无奈和沮丧、轻微的讽刺、无语的摇头
* **愤怒类场景**：愤怒和不满、生气的瞪视、暴躁的抓狂
* **惊讶类场景**：震惊的表情、意外的发现、困惑的思考
* **可爱类场景**：卖萌的表情、撒娇的动作、害羞的样子

### 情感关键词示例 [​](#情感关键词示例)

系统支持的情感关键词举例如下：

* 大笑、微笑、兴奋、手舞足蹈
* 无奈、沮丧、讽刺、无语、摇头
* 愤怒、不满、生气、瞪视、抓狂
* 震惊、意外、困惑、思考
* 卖萌、撒娇、害羞、可爱

### 匹配机制 [​](#匹配机制)

* **精确匹配**：优先匹配完整的场景描述，如"开心的大笑"
* **关键词匹配**：如果没有精确匹配，则根据关键词进行模糊匹配
* **语义匹配**：系统会理解场景的语义含义进行智能匹配

## 注意事项 [​](#注意事项)

1. **异步函数**：部分函数是异步的，需要使用 `await`
2. **返回格式**：表情包以base64编码返回，可直接用于发送
3. **错误处理**：所有函数都有错误处理，失败时返回None，空列表或默认值
4. **使用统计**：系统会记录表情包的使用次数
5. **文件依赖**：表情包依赖于本地文件，确保表情包文件存在
6. **编码格式**：返回的是base64编码的图片数据，可直接用于网络传输
7. **场景理解**：系统能理解具体的场景描述，比简单的情感分类更准确

最后更新:

Pager

[Previous page回复生成器API](/develop/plugin_develop/api/generator-api.md)

[Next page人物信息API](/develop/plugin_develop/api/person-api.md)