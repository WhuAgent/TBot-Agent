# TBot-Agent

## 安装与配置

Python 版本：`python = 3.10` 。

## 配置文件说明

**重要**：需要先根据模板文件 `config/openai_config.yaml.template` 创建对应的 openai API 配置文件，在文件里填上自己的 openai API key 和对应的 API base。

`config/actions` 文件夹是存放动作（命令）配置的地方，详见下文对如何新增命令提示词的描述。

## 项目运行

**重要：请以管理员身份运行 Pycharm**！否则无法对 TBot Studio 进行操作。

以管理员身份运行 Pycharm 之后，需要进行和 TBot Studio 相关的一些配置，详情参见 [如何让生成的代码能够自动运行](docs/tbot.md) 。

完成上述两步之后，在根目录下运行命令：

```
python -m tbot.main
```

## 如何新增动作（命令）提示词

详见 [如何新增动作（命令）](docs/add_action.md) 。

## 如何优雅地创建测试用例

虽然我们进行的不是真正的单元测试，但是这种实现方式允许我们方便地进行演示，不需要在 `if __name__ == "__main__"` 中对代码进行注释和清除注释操作，同时也使得代码更加结构化和模块化。此想法由 **@陈沛然 (prchen818)** 同学提出。

具体操作详见 [如何优雅地创建测试用例](docs/test.md) 。
