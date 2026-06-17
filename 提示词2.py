import os
from openai import OpenAI
from dotenv import load_dotenv

# 初始化DeepSeek客户端，加载密钥和地址
def init_client():
    load_dotenv()
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL")
    )

# 通用提问函数：传入提示词+自定义参数，调用大模型并打印结果
def ask(prompt, **params):
    client = init_client()
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        **({"temperature": 0.7, "max_tokens": 800} | params)
    )
    print(res.choices[0].message.content.strip())
    print("-" * 80)  # 加分隔线，区分不同问题的回答，更清晰

# 提示词模板1：角色代入式 - 指定身份完成任务
def role_based_prompt(role, task, requirements):
    return f"请以{role}的身份完成任务：{task}\n要求：\n" + "\n".join(f"- {req}" for req in requirements)

# 提示词模板2：分步分析式 - 按指定步骤完成分析
def step_by_step_prompt(task, steps):
    return f"任务：{task}\n请按步骤分析：\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))

# 提示词模板3：模板填充式 - 自定义模板动态传参
def template_based_prompt(template, **kwargs):
    return template.format(** kwargs)

# 程序入口：3个实战场景调用示例
if __name__ == "__main__":
    # 场景1：角色代入 - 资深产品经理评估社交功能
    role_prompt = role_based_prompt(
        role="资深产品经理",
        task="评估一个新的社交功能",
        requirements=["分析目标用户需求", "评估技术可行性", "预测潜在风险", "提出改进建议"]
    )
    ask(role_prompt)

    # 场景2：分步分析 - 电商网站用户增长策略
    step_prompt = step_by_step_prompt(
        task="电商网站用户增长策略",
        steps=["分析数据与瓶颈", "研究竞品策略", "提出增长方案", "设计时间表", "制定评估标准"]
    )
    ask(step_prompt)

    # 场景3：模板填充 - 智能健康手表营销策略
    tpl_content = "产品名称：{product}\n目标人群：{target}\n核心问题：{problem}\n请给出营销策略（定位/渠道/方案/预期效果）。"
    template_prompt = template_based_prompt(
        template=tpl_content,
        product="智能健康手表",
        target="25-45岁健康意识强的都市人群",
        problem="在竞争激烈市场中突出特色"
    )
    ask(template_prompt)  # 补全你缺失的这一行调用