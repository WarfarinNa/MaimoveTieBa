LLM API | MaiBot 文档中心



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

# LLM API [​](#llm-api)

LLM API模块提供与大语言模型交互的功能，让插件能够使用系统配置的LLM模型进行内容生成。

## 导入方式 [​](#导入方式)

python

```
from src.plugin_system.apis import llm_api
# 或者
from src.plugin_system import llm_api
```

## 主要功能 [​](#主要功能)

### 1. 查询可用模型 [​](#_1-查询可用模型)

python

```
def get_available_models() -> Dict[str, TaskConfig]:
```

获取所有可用的模型配置。

**Return：**

* `Dict[str, TaskConfig]`：模型配置字典，key为模型名称，value为模型配置对象。

### 2. 使用模型生成内容 [​](#_2-使用模型生成内容)

python

```
async def generate_with_model(
    prompt: str, model_config: TaskConfig, request_type: str = "plugin.generate", **kwargs
) -> Tuple[bool, str, str, str]:
```

使用指定模型生成内容。

**Args:**

* `prompt`：提示词。
* `model_config`：模型配置对象（从 `get_available_models` 获取）。
* `request_type`：请求类型标识，默认为 `"plugin.generate"`。
* `**kwargs`：其他模型特定参数，如 `temperature`、`max_tokens` 等。

**Return：**

* `Tuple[bool, str, str, str]`：返回一个元组，包含（是否成功, 生成的内容, 推理过程, 模型名称）。

最后更新:

Pager

[Previous page聊天流API](/develop/plugin_develop/api/chat-api.md)

[Next page回复生成器API](/develop/plugin_develop/api/generator-api.md)