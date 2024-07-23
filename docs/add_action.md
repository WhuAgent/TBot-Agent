# 如何新增动作（命令）

## 新增命令提示词的格式


所有命令都被放在 `config/actions` 目录下。

当要新建一个动作时，创建文件夹 `一级命令/二级命令/三级命令` （命名规范参考[动作任务分配表](https://u1tkb79ep4e.feishu.cn/sheets/QBuusFugZhUanitl6KLcFa8En8f)），在对应的文件夹下进行操作。

接下来以打开 Word 文档这一动作为例。

首先创建文件夹 `OfficeAutomation/Word/WordOpenDocument`。

在该文件夹下创建三个文件（**文件命名与函数命名均保持与 TBot 对应命令同步**）：

- `WordOpenDocument.prompt`: 提供给大模型的提示词。
- `WordOpenDocument.yaml`: 该动作在 TBot Studio 中对应命令参数和返回值的配置。
- `WordOpenDocument.py`: 该动作的实现逻辑，目前为生成对应 TBot 代码。

**配置完三个文件之后，在 `action_module_config.yaml` 添加命令对应的包路径**。这样解析器才能找到对应的命令。

每个文件具体如下所示：

### WordOpenDocument.prompt

```
def WordOpenDocument(file_path):
    """
    打开指定路径的文档
    ---
    参数：
        file_path: 指定的文档路径
    返回值：
        word_object: 打开的文档对象
    """
```

如上述样例所示，新增命令需要写成 python 函数的形式，包括函数名，函数参数，以及对函数的注释。
]
需要保证命名规范，以及注释规范（解释函数作用，每个参数的解释，以及返回值的解释），以给大模型准确的信息，减少大模型出错的概率。

### WordOpenDocument.yaml

```
args:
  show_word: 是
  file_path: ""
  unknown_args: 是
  pre_delay: 0
  post_delay: 0
  continue_when_error: False

rets:
  word_object: Word1
```

该 yaml 文件应当包含实际 TBot 命令中所有需要配置的参数与返回值，包括默认值（如果没有默认值就留空）。

### WordOpenDocument.py

```python
import yaml

from utils.function import function_args2str, function_rets2str
from utils.function import convert2double_slash_path

config_path = "config/actions/OfficeAutomation/Word/WordOpenDocument/WordOpenDocument.yaml"
with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def decorate_args(args):
    # 在这里写下每个命令参数的特殊处理
    file_path = convert2double_slash_path(args["file_path"])
    args["file_path"] = f'\"{file_path}\"'
    return args


def WordOpenDocument(args):
    args = decorate_args(args)
    args_str = function_args2str(config, args)
    rets_str = function_rets2str(config, args)
    return f"{rets_str} = WordOpenDocument({args_str})"
```

这里需要配置的有：

- line6 的 `config_path` 需要修改为对应的 yaml 文件路径。
- 函数名以及返回的字符串要改成 TBot 对应的命令名称。
- 如果命令没有返回值，可以删掉 line21。
- `decorate_args` 函数中写一些对参数进行预处理的逻辑，如把所有路径变成双斜杠等。