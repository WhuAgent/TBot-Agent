## TBot-Agent

### 安装与配置

Python 版本：`python = 3.10` 。

### 配置文件说明

**重要**：需要先根据模板文件 `config/openai_config.yaml.template` 创建对应的 openai API 配置文件，在文件里填上自己的 openai API key 和对应的 API base。

#### 运行 WebNavigation 项目须知（TBotAgent 项目不用管）

在 `config/config.yaml` 文件中，原来使用的时绝对路径表示 chormedriver 和 Miniwob 环境地址，所以在新机器上跑时需要重新配置，现在改为了相对路径，应该就不需要重新配置了。

因为本项目是从 WebNavigation 项目迁移而来，因此 `config/miniwob_tasks.yaml` 里展示了所有本项目支持的 Miniwob 任务，`config/succeed_envs.yaml` 用于防止已经研究完毕的环境下次启动之后再跑。

### 项目运行

运行项目之前，需要创建 `config/openai_config.yaml` 配置文件，并填入相关信息。

#### TBotAgent 项目

在根目录下运行命令：

```
python -m tbot.main
```

#### WebNavigation 项目（由于修改了文件结构，暂时无法运行）

在根目录下运行命令：

```
python -m model.main
```

#### 可能的报错

如果报错：无法访问 `log` 文件夹，那么就在根目录下新建一个 `log` 文件夹。

### 新增命令提示词的格式

```
def WordOpenDocument(self, file_path):
    """
    打开指定路径的文档
    ---
    参数：
        file_path: 指定的文档路径
    返回值：
        无返回值
    """
```

如上述样例所示，新增命令需要写成 python 函数的形式，包括函数名，函数参数，以及对函数的注释。

需要保证命名规范，以及注释规范（解释函数作用，每个参数的解释，以及返回值的解释），以给大模型准确的信息，减少大模型出错的概率。