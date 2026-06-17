import os
from openai import OpenAI
from dotenv import load_dotenv

# ========== 先补全 父类 PromptEngineer (必须有，子类继承依赖) ==========
class PromptEngineer:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url=os.getenv('DEEPSEEK_BASE_URL')
        )
        self.default_params = {
            'temperature': 0.7,
            'max_tokens': 2000,  # 调大token数，适配长推理过程
            'top_p': 1.0,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        }

    def generate_response(self, prompt, **kwargs):
        """生成响应的基础方法"""
        try:
            messages = [
                {"role": "system", "content": kwargs.pop('system_message', "You are a helpful assistant.")},
                {"role": "user", "content": prompt}
            ]
            history = kwargs.pop('history', [])
            if history:
                messages = history + messages
            params = {**self.default_params, **kwargs}
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,** params
            )
            return {
                'status': 'success',
                'content': response.choices[0].message.content,
                'message': response.choices[0].message
            }
        except Exception as e:
            print(f"Error details: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def clear_prompt(self, prompt):
        """清理和标准化提示词"""
        return prompt.strip()

    def format_prompt(self, template, **kwargs):
        """格式化提示词模板"""
        return template.format(** kwargs)

    def validate_prompt(self, prompt):
        """验证提示词是否符合基本要求"""
        return bool(prompt and prompt.strip())

# ========== 核心子类：思维链(Chain of Thought) 实现 ==========
class ChainOfThought(PromptEngineer):
    def __init__(self):
        super().__init__()  # 继承父类所有属性和方法

    def create_cot_prompt(self, task_description, question, cot_examples=None):
        """
        创建【标准思维链】提示词 - 自由分步推理，带示例参考
        :param task_description: 任务描述
        :param question: 待解决的问题
        :param cot_examples: 带推理过程的示例列表
        :return: 标准化的思维链提示词
        """
        prompt_parts = [
            f"任务说明: {task_description}\n",
            "请一步步思考并解决问题。每一步都要说明推理过程。\n"
        ]

        # 添加思维链示例（有示例则加，无则不加）
        if cot_examples:
            examples_text = "\n\n".join(
                f"问题: {ex['question']}\n思考过程:\n{ex['reasoning']}\n最终答案: {ex['answer']}"
                for ex in cot_examples
            )
            prompt_parts.append(f"示例：\n{examples_text}\n")

        # 拼接待解决的问题
        prompt_parts.append(f"现在，请解决以下问题：\n{question}\n\n思考过程：")
        return self.clear_prompt("\n".join(prompt_parts))

    def create_structured_cot_prompt(self, problem, steps):
        """
        创建【结构化思维链】提示词 - 按指定步骤强制推理，逻辑更严谨
        :param problem: 问题描述
        :param steps: 固定的推理步骤列表
        :return: 标准化的结构化思维链提示词
        """
        prompt = f"""问题：{problem}

请按照以下步骤进行分析和推理：
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(steps))}

对于每一步，请详细说明你的思考过程。
最后，给出最终的结论。"""
        return self.clear_prompt(prompt)

    def solve_with_cot(self, problem, approach='standard', **kwargs):
        """
        对外统一调用入口：使用思维链方法解决问题
        :param problem: 问题描述
        :param approach: 推理方式 standard(标准自由推理)/structured(指定步骤推理)
        :param kwargs: 扩展参数
        :return: 大模型返回结果
        """
        if approach not in ['standard', 'structured']:
            raise ValueError("支持的方法为'standard'和'structured'")

        # 结构化思维链：指定步骤推理
        if approach == 'structured':
            steps = kwargs.get('steps', [
                "理解问题关键信息",
                "分析可能的解决方案",
                "评估每个方案的可行性",
                "选择最佳方案",
                "制定具体实施步骤"
            ])
            prompt = self.create_structured_cot_prompt(problem, steps)
        # 标准思维链：自由分步推理
        else:
            task_description = kwargs.get('task_description', "请解决以下问题，并展示详细的思考过程。")
            cot_examples = kwargs.get('cot_examples', None)
            prompt = self.create_cot_prompt(task_description, problem, cot_examples)

        return self.generate_response(prompt)

# ========== 思维链调用演示 ==========
def cot_demo():
    """Chain of Thought 两种推理方式的示例演示"""
    cot = ChainOfThought()

    # 1. 标准CoT示例 - 数学促销最优解问题（自由推理）
    problem1 = """
一个商店进行促销活动：
- 买3件商品打8折
- 买5件商品打7折
- 单件商品原价100元
如果顾客想购买6件商品，应该如何购买最划算？
"""
    # 思维链示例：给大模型参考的推理格式
    cot_examples = [
        {
            "question": "如果一个数是7的倍数，同时也是3的倍数，这个数最小是多少？",
            "reasoning": """
1. 首先，我需要找到7的倍数：7, 14, 21, 28, 35...
2. 然后，我需要找到3的倍数：3, 6, 9, 12, 15, 18, 21...
3. 对比两个序列，找到第一个共同的数字
4. 可以看到21同时出现在两个序列中""",
            "answer": "21是同时满足条件的最小数"
        }
    ]

    # 2. 结构化CoT示例 - 项目管理工具选型（按指定步骤推理）
    problem2 = """
一个团队需要选择项目管理工具，已知：
- 团队规模20人
- 预算每人每月50元
- 需要任务管理和协作功能
- 要求有中文界面
请推荐合适的工具。
"""
    # 指定的固定推理步骤
    steps = [
        "分析团队需求和约束条件",
        "调研市场上的可用工具",
        "对比不同工具的功能和价格",
        "评估工具的优缺点",
        "给出最终推荐"
    ]

    # 测试1：标准思维链推理
    print("\n===== 1. 标准Chain of Thought(自由推理) 结果：=====")
    result1 = cot.solve_with_cot(
        problem1,
        'standard',
        task_description="请解决以下数学问题，展示详细的计算和推理过程，最后给出最优方案。",
        cot_examples=cot_examples
    )
    if result1.get('status') == 'success':
        print(result1['content'])
    else:
        print(f"Error: {result1.get('message','unknown error')}")

    # 测试2：结构化思维链推理
    print("\n===== 2. 结构化Chain of Thought(指定步骤推理) 结果：=====")
    result2 = cot.solve_with_cot(
        problem2,
        'structured',
        steps=steps
    )
    if result2.get('status') == 'success':
        print(result2['content'])
    else:
        print(f"Error: {result2.get('message','unknown error')}")

# ========== 程序入口 ==========
if __name__ == "__main__":
    cot_demo()