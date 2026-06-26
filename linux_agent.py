import sys
import shlex


COMMAND_EXPLANATIONS = {
    "ls": "查看目录下有哪些文件。",
    "cd": "切换当前所在目录。",
    "pwd": "显示当前所在目录。",
    "mkdir": "创建文件夹。",
    "rm": "删除文件或文件夹。",
    "cp": "复制文件或文件夹。",
    "mv": "移动文件或重命名文件。",
    "cat": "直接显示文件内容。",
    "less": "分页查看文件内容。",
    "grep": "在文本中搜索指定内容。",
    "find": "查找文件或文件夹。",
    "make": "编译当前项目。",
    "cmake": "生成项目编译配置。",
    "python3": "运行 Python 程序。",
    "export": "设置环境变量。",
    "echo": "输出一段文本。",
    "tee": "把内容显示在终端，同时保存到文件。",
    "ip": "查看或配置网络信息。",
    "ping": "测试网络是否连通。",
    "systemctl": "管理系统服务。",
    "sudo": "用管理员权限执行命令。",
    "apt": "Ubuntu/Debian 系统的软件安装与管理工具。",
}


OPTION_EXPLANATIONS = {
    "-l": "长格式显示，会显示权限、大小、时间等信息。",
    "-h": "用更容易读的单位显示大小，例如 K、M、G。",
    "-a": "显示所有文件，包括隐藏文件。",
    "-p": "父目录不存在时一起创建。",
    "-r": "递归处理目录及其子目录。",
    "-R": "递归处理目录及其子目录。",
    "-f": "强制执行，不进行确认。",
    "-i": "执行前逐个确认，比较安全。",
    "-v": "显示详细执行过程。",
}


SPECIAL_SYMBOLS = {
    "|": "管道符：把前一个命令的输出，交给后一个命令继续处理。",
    ">": "重定向：把输出写入文件，会覆盖原文件。",
    ">>": "追加重定向：把输出追加写入文件，不覆盖原文件。",
    "2>&1": "把错误输出 stderr 合并到普通输出 stdout。",
}


DANGEROUS_PATTERNS = [
    "rm -rf",
    "rm -fr",
    "sudo rm",
    "chmod 777",
    "mkfs",
    "dd ",
]


def check_danger(command_text):
    print("\n三、风险提醒")

    found = False

    for pattern in DANGEROUS_PATTERNS:
        if pattern in command_text:
            found = True
            print(f"⚠️ 发现危险片段：{pattern}")

    if found:
        print("这条命令有风险，执行前一定要确认路径是否正确。")
        print("尤其是 rm、sudo rm、dd、mkfs 这类命令，可能会删除文件或破坏磁盘。")
    else:
        print("没有发现明显危险片段。")


def explain_option(option):
    if option in OPTION_EXPLANATIONS:
        print(f"{option}：{OPTION_EXPLANATIONS[option]}")
        return

    # 处理 -lh 这种组合参数
    if option.startswith("-") and not option.startswith("--") and len(option) > 2:
        print(f"{option}：这是组合参数，可以拆开理解：")
        for char in option[1:]:
            single_option = "-" + char
            if single_option in OPTION_EXPLANATIONS:
                print(f"  {single_option}：{OPTION_EXPLANATIONS[single_option]}")
            else:
                print(f"  {single_option}：暂时没有收录这个选项的解释。")
        return

    if option.startswith("-"):
        print(f"{option}：这是一个选项参数，具体含义需要结合主命令查看。")
    else:
        print(f"{option}：这是操作对象，可能是文件、文件夹、文本或路径。")


def split_by_pipe(parts):
    commands = []
    current = []

    for item in parts:
        if item == "|":
            commands.append(current)
            current = []
        else:
            current.append(item)

    if current:
        commands.append(current)

    return commands


def explain_single_command(parts, index=None):
    if not parts:
        return

    main_cmd = parts[0]

    if index is not None:
        print(f"\n第 {index} 个命令：")
    else:
        print("\n一、主命令")

    print(f"主命令是：{main_cmd}")

    if main_cmd in COMMAND_EXPLANATIONS:
        print(f"作用：{COMMAND_EXPLANATIONS[main_cmd]}")
    elif main_cmd.startswith("./"):
        print("作用：运行当前目录下的一个可执行程序。")
    else:
        print("作用：这个命令暂时还没有收录，后面可以继续扩展。")

    if len(parts) == 1:
        print("参数：没有额外参数。")
        return

    print("参数分析：")
    skip_next = False

    for i, item in enumerate(parts[1:]):
        if skip_next:
            skip_next = False
            continue

        if item in SPECIAL_SYMBOLS:
            print(f"{item}：{SPECIAL_SYMBOLS[item]}")

            # > 和 >> 后面一般跟文件名
            if item in [">", ">>"] and i + 2 <= len(parts[1:]):
                skip_next = True
            continue

        if item == "2>&1":
            print(f"{item}：{SPECIAL_SYMBOLS[item]}")
            continue

        explain_option(item)


def analyze_command(command_text):
    print("=" * 60)
    print("Linux 命令解释 Agent v2")
    print("=" * 60)

    print("\n你输入的命令是：")
    print(command_text)

    try:
        parts = shlex.split(command_text)
    except ValueError:
        print("\n命令解析失败，可能是引号没有闭合。")
        return

    if len(parts) == 0:
        print("\n你没有输入命令。")
        return

    print("\n一、命令整体结构")

    if "|" in parts:
        print("这是一条带管道的命令。")
        print("可以理解为：前一个命令的输出结果，会交给后一个命令继续处理。")

        commands = split_by_pipe(parts)

        print("\n二、分段解释")
        for i, cmd_parts in enumerate(commands, start=1):
            explain_single_command(cmd_parts, i)
    else:
        print("这是一条普通命令。")
        print("\n二、命令解释")
        explain_single_command(parts)

    check_danger(command_text)

    print("\n四、整体理解")

    if command_text == "make 2>&1 | tee error.log":
        print("这条命令的意思是：编译项目，把普通输出和错误输出都显示在终端，同时保存到 error.log 文件中。")
    elif parts[0] == "ls":
        print("这条命令的意思是：查看指定目录里的文件。")
    elif parts[0] == "make":
        print("这条命令的意思是：编译当前项目。")
    else:
        print("这条命令的意思是：执行一个 Linux 操作，并根据后面的参数决定具体行为。")


def interactive_mode():
    print("=" * 60)
    print("Linux 命令解释 Agent 交互模式")
    print("=" * 60)
    print("输入一条 Linux 命令，我会帮你解释。")
    print("输入 exit 或 quit 可以退出程序。")

    while True:
        command = input("\n请输入 Linux 命令：")

        if command.strip() == "":
            print("你没有输入内容，请重新输入。")
            continue

        if command.strip() in ["exit", "quit"]:
            print("已退出 Linux 命令解释 Agent。")
            break

        analyze_command(command)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        command = " ".join(sys.argv[1:])
        analyze_command(command)
    else:
        interactive_mode()