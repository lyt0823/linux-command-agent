import os
import sys
from openai import OpenAI


def ask_deepseek(command_text):
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print("没有找到 DEEPSEEK_API_KEY。")
        print("请先在终端设置：")
        print('export DEEPSEEK_API_KEY="你的 DeepSeek API Key"')
        return

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    system_prompt = """
你是一个 Linux 命令解释 Agent。

你的任务：
1. 解释用户输入的 Linux 命令在做什么。
2. 拆解主命令、参数、路径、管道、重定向等部分。
3. 判断这条命令是否有风险。
4. 如果有风险，要明确提醒风险在哪里。
5. 不要真的执行命令，只分析文本。
6. 用户是 Linux 初学者，解释要通俗，不要太抽象。

输出格式固定为：
一、命令作用
二、结构拆解
三、风险判断
四、建议
"""

    user_prompt = f"""
请分析下面这条 Linux 命令：

{command_text}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            }
        )

        answer = response.choices[0].message.content
        print(answer)

    except Exception as e:
        print("调用 DeepSeek 失败。")
        print("错误信息：")
        print(e)


def interactive_mode():
    print("=" * 60)
    print("DeepSeek Linux 命令解释 Agent")
    print("=" * 60)
    print("输入 Linux 命令，我会交给 DeepSeek 分析。")
    print("输入 exit 或 quit 退出。")

    while True:
        command = input("\n请输入 Linux 命令：")

        if command.strip() == "":
            print("你没有输入内容。")
            continue

        if command.strip() in ["exit", "quit"]:
            print("已退出。")
            break

        ask_deepseek(command)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        command = " ".join(sys.argv[1:])
        ask_deepseek(command)
    else:
        interactive_mode()