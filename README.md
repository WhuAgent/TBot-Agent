# TBot-Agent

## 安装与配置

Python 版本：`python = 3.10` 。

对于 `agent-network` 库，请使用以下命令进行安装：

```
pip install git+https://github.com/WhuAgent/agent-network.git@d12c192259680462286d6609cc0615a898f6b93d
```

## 项目运行

```
python main.py
```

暂时还没有配置生成的代码自动粘贴，前期我们先采用手动粘贴的方式。

## 配置文件说明

`config/actions` 文件夹是存放动作（命令）配置的地方，详见下文对如何新增命令提示词的描述。

另外：对于框架内 pipeline、group、agent 的三级配置，详见 [Agent 网络开发文档](https://u1tkb79ep4e.feishu.cn/docx/Fwnrdnx9VoDkEZx0sEhcXtDYnbd) 。

## 如何新增动作（命令）提示词

详见 [TBotAgent 命令（服务）格式](https://u1tkb79ep4e.feishu.cn/docx/Ifo3dcqaZoT1n9xIvWicpKnbnf3) 。
