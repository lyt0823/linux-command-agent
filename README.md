[Uploading README.md…]()
# Linux 命令解释 Agent

这是一个用于解释 Linux 命令的小型 Agent。
用户输入一条 Linux 命令后，程序会调用 DeepSeek API，对命令进行解释、结构拆解、风险判断，并给出使用建议。

当前项目包含两个版本：

1. `linux_agent.py`：本地规则版，不联网，不消耗 API 额度，但解释能力较简单。
2. `deepseek_linux_agent.py`：DeepSeek 智能版，调用大模型进行解释，效果更好。

---

## 一、项目路径

本项目放在：

```bash
~/workspace/my_agent/linux_command_agent
```

进入项目目录：

```bash
cd ~/workspace/my_agent/linux_command_agent
```

---

## 二、创建并进入虚拟环境

首次使用时，建议在项目目录中创建 Python 虚拟环境：

```bash
python3 -m venv .venv
```

激活虚拟环境：

```bash
source .venv/bin/activate
```

激活后，终端前面会出现：

```bash
(.venv)
```

例如：

```bash
(.venv) (base) zdl@dell:~/workspace/my_agent/linux_command_agent$
```

---

## 三、安装依赖

DeepSeek API 兼容 OpenAI SDK，因此需要安装 `openai` 包：

```bash
python3 -m pip install --upgrade pip
python3 -m pip install openai
```

---

## 四、设置 DeepSeek API Key

使用 DeepSeek 智能版前，需要先设置 API Key。

在终端输入：

```bash
export DEEPSEEK_API_KEY="你的DeepSeek API Key"
```

例如：

```bash
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

检查是否设置成功：

```bash
echo $DEEPSEEK_API_KEY
```

如果能显示你的 Key，说明设置成功。

注意：不要把 API Key 写进代码里，也不要上传到 GitHub。

---

## 五、处理代理问题

如果运行时出现类似错误：

```text
ValueError: Unknown scheme for proxy URL URL('socks://127.0.0.1:7897/')
```

说明当前终端中存在 Python 不识别的代理设置。

可以先取消代理：

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
```

然后重新运行程序。

如果必须使用代理，可以安装 socks 支持：

```bash
python3 -m pip install "httpx[socks]"
```

并把代理地址设置为 `socks5://`，不要使用 `socks://`。

---

## 六、运行方式一：直接分析一条命令

使用 DeepSeek 智能版：

```bash
python3 deepseek_linux_agent.py "ls -lh ~/workspace"
```

示例：

```bash
python3 deepseek_linux_agent.py "make 2>&1 | tee error.log"
```

程序会解释：

* `make` 表示编译项目；
* `2>&1` 表示把错误输出合并到普通输出；
* `|` 表示管道；
* `tee error.log` 表示一边在终端显示，一边保存到 `error.log` 文件。

---

## 七、运行方式二：进入交互模式

直接运行：

```bash
python3 deepseek_linux_agent.py
```

进入交互模式后，可以连续输入 Linux 命令：

```bash
ls -lh ~/workspace
```

```bash
make 2>&1 | tee error.log
```

```bash
rm -rf build
```

程序会逐条解释命令，并判断是否存在风险。

退出交互模式：

```bash
exit
```

或者：

```bash
quit
```

---

## 八、本地规则版使用方法

如果不想调用 DeepSeek，也可以使用本地规则版：

```bash
python3 linux_agent.py "ls -lh ~/workspace"
```

进入本地规则版交互模式：

```bash
python3 linux_agent.py
```

本地规则版不需要 API Key，也不消耗额度，但只能解释代码里已经写好的常见命令。

---

## 九、完整使用流程

每次新开终端后，可以按下面流程使用：

```bash
cd ~/workspace/my_agent/linux_command_agent
source .venv/bin/activate
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
export DEEPSEEK_API_KEY="你的DeepSeek API Key"
python3 deepseek_linux_agent.py
```

进入交互模式后，直接输入需要解释的 Linux 命令即可。

---

## 十、常见问题

### 1. 报错：找不到 deepseek_linux_agent.py

错误示例：

```text
python3: can't open file 'deepseek_linux_agent.py': [Errno 2] No such file or directory
```

原因：当前目录不对，或者文件还没有创建。

解决方法：

```bash
cd ~/workspace/my_agent/linux_command_agent
ls
```

确认当前目录下是否有：

```text
deepseek_linux_agent.py
```

---

### 2. 报错：No module named openai

原因：当前虚拟环境里没有安装 `openai` 包。

解决方法：

```bash
source .venv/bin/activate
python3 -m pip install openai
```

---

### 3. 报错：没有找到 DEEPSEEK_API_KEY

原因：没有设置 DeepSeek API Key。

解决方法：

```bash
export DEEPSEEK_API_KEY="你的DeepSeek API Key"
```

---

### 4. 报错：Unknown scheme for proxy URL

原因：系统代理写成了 `socks://`，Python 不识别。

解决方法：

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
```

然后重新运行程序。

---

## 十一、项目当前功能

当前 Agent 已实现：

* 接收用户输入的 Linux 命令；
* 调用 DeepSeek API 进行分析；
* 解释命令整体作用；
* 拆解主命令、参数、路径、管道、重定向；
* 判断是否存在危险操作；
* 给出使用建议；
* 支持单条命令模式；
* 支持交互模式。

---

## 十二、后续可扩展方向

后续可以继续升级：

1. 增加命令历史记录；
2. 自动保存每次分析结果；
3. 增加报错日志分析功能；
4. 支持解释 `error.log` 文件；
5. 增加图形界面；
6. 支持语音输入；
7. 支持连接更多模型，例如 OpenAI、通义千问、智谱等。

---

## 十三、退出虚拟环境

使用结束后，可以退出虚拟环境：

```bash
deactivate
```
