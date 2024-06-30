## TBot-Agent

### 安装与配置

Python 版本：`python = 3.10` 。

### 配置文件说明

在 `config/config.yaml` 文件中，原来使用的时绝对路径表示 chormedriver 和 Miniwob 环境地址，所以在新机器上跑时需要重新配置，现在改为了相对路径，应该就不需要重新配置了。

**重要**：需要先根据模板文件 `config/openai_config.yaml.template` 创建对应的 openai API 配置文件，在文件里填上自己的 openai API key 和对应的 API base。

因为本项目是从 WebNavigation 项目迁移而来，因此 `config/miniwob_tasks.yaml` 里展示了所有本项目支持的 Miniwob 任务，`config/succeed_envs.yaml` 用于防止已经研究完毕的环境下次启动之后再跑。

### 项目运行

首先创建 `config/openai_config.yaml` 配置文件，并填入相关信息，然后即可在根目录下通过以下命令运行项目。

```
python -m model.main
```

如果报错：无法访问 `log` 文件夹，那么就在根目录下新建一个 `log` 文件夹。

### 新增命令提示词的格式

```
def find_element(self, start_ref_id, tag, content, **attribute):
    """
    从 ref 属性为 start_ref_id 的元素（0 表示根节点）开始，寻找距离该元素最近的，满足条件为（tag, content, attribute）的元素。
    其中：
    - start_ref_id 会在搜索结果中呈现，start_ref_id 为 0 表示 DOM 树的根节点。
    - tag 表示要寻找元素的标签。
    - content 表示元素上的文本，如果不关注文本，则 content 应为空字符串。
    - attribute 是一个字典，表示元素应有的属性和属性值，如果不关注元素属性，则 attribute 应为空字典。
    返回值：
    一个整数的列表，代表找到的元素的 ref id，如果后续接 click 或 type 动作代表直接对这些元素进行操作，也可以基于已经找到的 ref id 进行下一步的查找。
    """
```

如上述样例所示，新增命令需要写成 python 函数的形式，包括函数名，函数参数，以及对函数的注释。

需要保证命名规范，以及注释规范（解释函数作用，每个参数的解释，以及返回值的解释），以给大模型准确的信息，减少大模型出错的概率。