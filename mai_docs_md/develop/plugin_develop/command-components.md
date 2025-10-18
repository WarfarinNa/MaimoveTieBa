💻 Command组件详解 | MaiBot 文档中心



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

# 💻 Command组件详解 [​](#💻-command组件详解)

## 📖 什么是Command [​](#📖-什么是command)

Command是直接响应用户明确指令的组件，与Action不同，Command是**被动触发**的，当用户输入特定格式的命令时立即执行。

Command通过正则表达式匹配用户输入，提供确定性的功能服务。

### 🎯 Command的特点 [​](#🎯-command的特点)

* 🎯 **确定性执行**：匹配到命令立即执行，无随机性
* ⚡ **即时响应**：用户主动触发，快速响应
* 🔍 **正则匹配**：通过正则表达式精确匹配用户输入
* 🛑 **拦截控制**：可以控制是否阻止消息继续处理
* 📝 **参数解析**：支持从用户输入中提取参数

---

## 🛠️ Command组件的基本结构 [​](#🛠️-command组件的基本结构)

首先，Command组件需要继承自`BaseCommand`类，并实现必要的方法。

python

```
class ExampleCommand(BaseCommand):
    command_name = "example" # 命令名称，作为唯一标识符
    command_description = "这是一个示例命令" # 命令描述
    command_pattern = r"" # 命令匹配的正则表达式

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        """
        执行Command的主要逻辑

        Returns:
            Tuple[bool, str, bool]: 
                - 第一个bool表示是否成功执行
                - 第二个str是执行结果消息
                - 第三个bool表示是否需要阻止消息继续处理
        """
        # ---- 执行命令的逻辑 ----
        return True, "执行成功", False
```

**`command_pattern`**: 该Command匹配的正则表达式，用于精确匹配用户输入。

请注意：如果希望能获取到命令中的参数，请在正则表达式中使用有命名的捕获组，例如`(?P<param_name>pattern)`。

这样在匹配时，内部实现可以使用`re.match.groupdict()`方法获取到所有捕获组的参数，并以字典的形式存储在`self.matched_groups`中。

### 匹配样例 [​](#匹配样例)

假设我们有一个命令`/example param1=value1 param2=value2`，对应的正则表达式可以是：

python

```
class ExampleCommand(BaseCommand):
    command_name = "example"
    command_description = "这是一个示例命令"
    command_pattern = r"/example (?P<param1>\w+) (?P<param2>\w+)"

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        # 获取匹配的参数
        param1 = self.matched_groups.get("param1")
        param2 = self.matched_groups.get("param2")
        
        # 执行逻辑
        return True, f"参数1: {param1}, 参数2: {param2}", False
```

---

## Command 内置方法说明 [​](#command-内置方法说明)

python

```
class BaseCommand:
    def get_config(self, key: str, default=None):
        """获取插件配置值，使用嵌套键访问"""

    async def send_text(self, content: str, reply_to: str = "") -> bool:
        """发送回复消息"""

    async def send_type(self, message_type: str, content: str, display_message: str = "", typing: bool = False, reply_to: str = "") -> bool:
        """发送指定类型的回复消息到当前聊天环境"""

    async def send_command(self, command_name: str, args: Optional[dict] = None, display_message: str = "", storage_message: bool = True) -> bool:
        """发送命令消息"""

    async def send_emoji(self, emoji_base64: str) -> bool:
        """发送表情包"""

    async def send_image(self, image_base64: str) -> bool:
        """发送图片"""
```

具体参数与用法参见`BaseCommand`基类的定义。

最后更新:

Pager

[Previous pageActions系统](/develop/plugin_develop/action-components.md)

[Next page工具系统](/develop/plugin_develop/tool-components.md)