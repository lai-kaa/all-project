import os
import random
from openai import OpenAI
from dotenv import load_dotenv


# 初始化DeepSeek客户端 - 加载密钥和接口地址
def init_client():
    load_dotenv()
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL")
    )


# 核心：构建小样本(Few-Shot)提示词 - 给示例、定格式、标准化
def build_few_shot_prompt(task_description, examples, query):
    # 拼接所有示例：输入+输出的标准化格式
    examples_text = "\n\n".join(f"输入: {ex['input']}\n输出: {ex['output']}" for ex in examples)
    # 组装完整提示词，严格固定格式
    return f"""任务说明: {task_description}

示例：
{examples_text}

现在处理：
输入: {query}
输出:"""


# 通用提问函数 - 调用大模型+打印结果
def ask(prompt):
    client = init_client()
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    print(res.choices[0].message.content.strip())


# 程序入口 - 情感分析小样本实战
if __name__ == "__main__":
    # 1. 定义任务说明：明确告诉大模型要做什么
    task = "对文本进行情感分析，判断倾向（积极/消极/中性），并提取关键词"

    # 2. 定义示例样本：3个输入输出对照，大模型参考这个格式输出
    examples = [
        {"input": "这个产品质量很好，用着很满意", "output": "积极；关键词：质量好、满意"},
        {"input": "服务态度差，完全不推荐", "output": "消极；关键词：态度差、不推荐"},
        {"input": "价格合理，但是送货有点慢", "output": "中性；关键词：价格合理、送货慢"},
    ]

    # 3. 待分析的新句子
    query = "这家店的食物美味，但是价格有点贵"

    # 4. 构建提示词+调用大模型
    prompt = build_few_shot_prompt(task, examples, query)
    ask(prompt)