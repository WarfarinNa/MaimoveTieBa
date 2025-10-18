📦 插件依赖管理系统 | MaiBot 文档中心



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

# 📦 插件依赖管理系统 [​](#📦-插件依赖管理系统)

现在的Python依赖包管理依然存在问题，请保留你的`python_dependencies`属性，等待后续重构。

## 📚 详细教程 [​](#📚-详细教程)

### PythonDependency 类详解 [​](#pythondependency-类详解)

`PythonDependency`是依赖声明的核心类：

python

```
PythonDependency(
    package_name="PIL",          # 导入时的包名
    version=">=11.2.0",          # 版本要求
    optional=False,              # 是否为可选依赖
    description="图像处理库",     # 依赖描述
    install_name="pillow"        # pip安装时的包名（可选）
)
```

#### 参数说明 [​](#参数说明)

| 参数 | 类型 | 必需 | 说明 |
| --- | --- | --- | --- |
| `package_name` | str | ✅ | Python导入时使用的包名（如`requests`） |
| `version` | str | ❌ | 版本要求，使用pip格式（如`>=1.0.0`, `==2.1.3`） |
| `optional` | bool | ❌ | 是否为可选依赖，默认`False` |
| `description` | str | ❌ | 依赖的用途描述 |
| `install_name` | str | ❌ | pip安装时的包名，默认与`package_name`相同，用于处理安装名称和导入名称不一致的情况 |

#### 版本格式示例 [​](#版本格式示例)

python

```
# 常用版本格式
PythonDependency("requests", ">=2.25.0")           # 最小版本
PythonDependency("numpy", ">=1.20.0,<2.0.0")       # 版本范围
PythonDependency("pillow", "==8.3.2")              # 精确版本
PythonDependency("scipy", ">=1.7.0,!=1.8.0")       # 排除特定版本
```

最后更新:

Pager

[Previous page配置管理指南](/develop/plugin_develop/configuration-guide.md)

[Next page发送API](/develop/plugin_develop/api/send-api.md)