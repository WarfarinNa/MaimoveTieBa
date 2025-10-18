🔧 工具组件详解 | MaiBot 文档中心



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

# 🔧 工具组件详解 [​](#🔧-工具组件详解)

## 📖 什么是工具 [​](#📖-什么是工具)

工具是MaiBot的信息获取能力扩展组件。如果说Action组件功能五花八门，可以拓展麦麦能做的事情，那么Tool就是在某个过程中拓宽了麦麦能够获得的信息量。

### 🎯 工具的特点 [​](#🎯-工具的特点)

* 🔍 **信息获取增强**：扩展麦麦获取外部信息的能力
* 📊 **数据丰富**：帮助麦麦获得更多背景信息和实时数据
* 🔌 **插件式架构**：支持独立开发和注册新工具
* ⚡ **自动发现**：工具会被系统自动识别和注册

### 🆚 Tool vs Action vs Command 区别 [​](#🆚-tool-vs-action-vs-command-区别)

| 特征 | Action | Command | Tool |
| --- | --- | --- | --- |
| **主要用途** | 扩展麦麦行为能力 | 响应用户指令 | 扩展麦麦信息获取 |
| **触发方式** | 麦麦智能决策 | 用户主动触发 | LLM根据需要调用 |
| **目标** | 让麦麦做更多事情 | 提供具体功能 | 让麦麦知道更多信息 |
| **使用场景** | 增强交互体验 | 功能服务 | 信息查询和分析 |

## 🏗️ Tool组件的基本结构 [​](#🏗️-tool组件的基本结构)

每个工具必须继承 `BaseTool` 基类并实现以下属性和方法：

python

```
from src.plugin_system import BaseTool

class MyTool(BaseTool):
    # 工具名称，必须唯一
    name = "my_tool"
    
    # 工具描述，告诉LLM这个工具的用途
    description = "这个工具用于获取特定类型的信息"
    
    # 参数定义，仅定义参数
    # 比如想要定义一个类似下面的openai格式的参数表，则可以这么定义:
    # {
    #     "type": "object",
    #     "properties": {
    #         "query": {
    #             "type": "string",
    #             "description": "查询参数"
    #         },
    #         "limit": {
    #             "type": "integer", 
    #             "description": "结果数量限制"
    #         }
    #     },
    #     "required": ["query"]
    # }
    parameters = [
        ("query", "string", "查询参数", True),  # 必填参数
        ("limit", "integer", "结果数量限制", False)  # 可选参数
    ]

    available_for_llm = True  # 是否对LLM可用
    
    async def execute(self, function_args: Dict[str, Any]):
        """执行工具逻辑"""
        # 实现工具功能
        result = f"查询结果: {function_args.get('query')}"
        
        return {
            "name": self.name,
            "content": result
        }
```

### 属性说明 [​](#属性说明)

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `name` | str | 工具的唯一标识名称 |
| `description` | str | 工具功能描述，帮助LLM理解用途 |
| `parameters` | list[tuple] | 参数定义 |

其构造而成的工具定义为:

python

```
{"name": cls.name, "description": cls.description, "parameters": cls.parameters}
```

### 方法说明 [​](#方法说明)

| 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| `execute` | `function_args` | `dict` | 执行工具核心逻辑 |

---

## 🎨 完整工具示例 [​](#🎨-完整工具示例)

完成一个天气查询工具

python

```
from src.plugin_system import BaseTool
import aiohttp
import json

class WeatherTool(BaseTool):
    """天气查询工具 - 获取指定城市的实时天气信息"""
    
    name = "weather_query"
    description = "查询指定城市的实时天气信息，包括温度、湿度、天气状况等"
    available_for_llm = True  # 允许LLM调用此工具
    parameters = [
        ("city", "string", "要查询天气的城市名称，如：北京、上海、纽约", True),
        ("country", "string", "国家代码，如：CN、US，可选参数", False)
    ]
    
    async def execute(self, function_args: dict):
        """执行天气查询"""
        try:
            city = function_args.get("city")
            country = function_args.get("country", "")
            
            # 构建查询参数
            location = f"{city},{country}" if country else city
            
            # 调用天气API（示例）
            weather_data = await self._fetch_weather(location)
            
            # 格式化结果
            result = self._format_weather_data(weather_data)
            
            return {
                "name": self.name,
                "content": result
            }
            
        except Exception as e:
            return {
                "name": self.name,
                "content": f"天气查询失败: {str(e)}"
            }
    
    async def _fetch_weather(self, location: str) -> dict:
        """获取天气数据"""
        # 这里是示例，实际需要接入真实的天气API
        api_url = f"http://api.weather.com/v1/current?q={location}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                return await response.json()
    
    def _format_weather_data(self, data: dict) -> str:
        """格式化天气数据"""
        if not data:
            return "暂无天气数据"
        
        # 提取关键信息
        city = data.get("location", {}).get("name", "未知城市")
        temp = data.get("current", {}).get("temp_c", "未知")
        condition = data.get("current", {}).get("condition", {}).get("text", "未知")
        humidity = data.get("current", {}).get("humidity", "未知")
        
        # 格式化输出
        return f"""
🌤️ {city} 实时天气
━━━━━━━━━━━━━━━━━━
🌡️ 温度: {temp}°C
☁️ 天气: {condition}
💧 湿度: {humidity}%
━━━━━━━━━━━━━━━━━━
        """.strip()
```

---

## 🚨 注意事项和限制 [​](#🚨-注意事项和限制)

### 当前限制 [​](#当前限制)

1. **适用范围**：主要适用于信息获取场景
2. **配置要求**：必须开启工具处理器

### 开发建议 [​](#开发建议)

1. **功能专一**：每个工具专注单一功能
2. **参数明确**：清晰定义工具参数和用途
3. **错误处理**：完善的异常处理和错误反馈
4. **性能考虑**：避免长时间阻塞操作
5. **信息准确**：确保获取信息的准确性和时效性

## 🎯 最佳实践 [​](#🎯-最佳实践)

### 1. 工具命名规范 [​](#_1-工具命名规范)

#### ✅ 好的命名 [​](#✅-好的命名)

python

```
name = "weather_query"        # 清晰表达功能
name = "knowledge_search"     # 描述性强
name = "stock_price_check"    # 功能明确
```

#### ❌ 避免的命名 [​](#❌-避免的命名)

python

```
name = "tool1"               # 无意义
name = "wq"                  # 过于简短
name = "weather_and_news"    # 功能过于复杂
```

### 2. 描述规范 [​](#_2-描述规范)

#### ✅ 良好的描述 [​](#✅-良好的描述)

python

```
description = "查询指定城市的实时天气信息，包括温度、湿度、天气状况"
```

#### ❌ 避免的描述 [​](#❌-避免的描述)

python

```
description = "天气"         # 过于简单
description = "获取信息"      # 不够具体
```

### 3. 参数设计 [​](#_3-参数设计)

#### ✅ 合理的参数设计 [​](#✅-合理的参数设计)

python

```
parameters = [
    ("city", "string", "城市名称，如：北京、上海", True),
    ("unit", "string", "温度单位：celsius 或 fahrenheit", False)
]
```

#### ❌ 避免的参数设计 [​](#❌-避免的参数设计)

python

```
parameters = [
    ("data", "string", "数据", True)  # 参数过于模糊
]
```

### 4. 结果格式化 [​](#_4-结果格式化)

#### ✅ 良好的结果格式 [​](#✅-良好的结果格式)

python

```
def _format_result(self, data):
    return f"""
🔍 查询结果
━━━━━━━━━━━━
📊 数据: {data['value']}
📅 时间: {data['timestamp']}
📝 说明: {data['description']}
━━━━━━━━━━━━
    """.strip()
```

#### ❌ 避免的结果格式 [​](#❌-避免的结果格式)

python

```
def _format_result(self, data):
    return str(data)  # 直接返回原始数据
```

最后更新:

Pager

[Previous page命令处理系统](/develop/plugin_develop/command-components.md)

[Next page配置管理指南](/develop/plugin_develop/configuration-guide.md)