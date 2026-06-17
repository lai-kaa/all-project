import os
from openai import OpenAI
from dotenv import load_dotenv

# ===================== 基础提示词工程+大模型调用类 =====================
class PromptEngineer:
    def __init__(self):
        # 加载.env文件中的配置（密钥/地址）
        load_dotenv()
        # 创建OpenAI客户端，兼容DeepSeek API调用
        self.client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url=os.getenv('DEEPSEEK_BASE_URL')
        )
        # 大模型默认生成参数，可被外部传入参数覆盖
        self.default_params = {
            'temperature': 0.7,      # 随机性：0(严谨)~2(放飞)
            'max_tokens': 1000,       # 最大生成字符数
            'top_p': 1.0,             # 采样策略：1.0为不限制
            'frequency_penalty': 0.0, # 重复度惩罚：越大越不重复
            'presence_penalty': 0.0   # 新内容奖励：越大越易出新内容
        }

    def generate_response(self, prompt, **kwargs):
        """生成响应的基础方法 - 单次调用，返回完整结果"""
        try:
            # 构建消息体：系统指令 + 用户提问
            messages = [
                {"role": "system", "content": kwargs.pop('system_message', "You are a helpful assistant.")},
                {"role": "user", "content": prompt}
            ]
            # 拼接历史对话（可选）
            history = kwargs.pop('history', [])
            if history:
                messages = history + messages
            # 合并默认参数和自定义参数
            params = {**self.default_params, **kwargs}
            # 发起API调用
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                **params
            )
            # 返回标准化结果
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
        """清理和标准化提示词 - 去除首尾空格换行"""
        return prompt.strip()

    def format_prompt(self, template, **kwargs):
        """格式化提示词模板 - 传模板+参数，自动填充"""
        return template.format(**kwargs)

    def validate_prompt(self, prompt):
        """验证提示词是否有效 - 非空校验"""
        return bool(prompt and prompt.strip())

    def generate_stream_response(self, prompt, **kwargs):
        """生成流式响应的方法 - 边生成边返回，打字机效果"""
        try:
            messages = [
                {"role": "system", "content": kwargs.pop('system_message', "You are a helpful assistant.")},
                {"role": "user", "content": prompt}
            ]
            history = kwargs.pop('history', [])
            if history:
                messages = history + messages
            # 流式调用核心参数：stream=True
            return self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True,
                **kwargs
            )
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def create_function_prompt(self, task, function_name, parameters):
        """创建函数调用提示词 - 标准化生成函数调用指令"""
        prompt = f"""任务：{task}
请使用以下函数完成任务：
函数名称：{function_name}
参数说明：
{chr(10).join(f'- {k}: {v}' for k, v in parameters.items())}
请返回合适的函数调用参数。"""
        return self.clear_prompt(prompt)

# ===================== 进阶提示词工程类（继承基础类） =====================
class AdvancedPromptEngineer(PromptEngineer):
    def __init__(self):
        super().__init__()  # 继承父类的所有属性和方法

    def create_clarity_prompt(self, task_description, requirements):
        """清晰性原则 - 指令清晰、要求明确"""
        prompt = f"""任务说明：{task_description}
具体要求：
{chr(10).join(f'{i+1}. {req}' for i, req in enumerate(requirements))}
请按照上述要求提供详细的回答。"""
        return self.clear_prompt(prompt)

    def create_specific_prompt(self, task, constraints):
        """具体性原则 - 任务具体、限制明确"""
        prompt = f"""任务详情：
{chr(10).join(f'- {k}: {v}' for k, v in task.items())}
限制条件：
{chr(10).join(f'- {k}: {v}' for k, v in constraints.items())}
请严格按照以上要求完成任务。"""
        return self.clear_prompt(prompt)

    def create_context_prompt(self, context, question):
        """上下文原则 - 补充背景，基于上下文回答"""
        prompt = f"""背景信息：
{chr(10).join(f'- {k}: {v}' for k, v in context.items())}
问题：{question}
请基于上述背景信息回答问题。"""
        return self.clear_prompt(prompt)

    def create_example_prompt(self, task, examples):
        """示例提供原则 - 给参考示例，规范输出格式"""
        examples_text = "\n\n".join(
            f"示例 {i+1}:\n输入: {ex['input']}\n输出: {ex['output']}"
            for i, ex in enumerate(examples)
        )
        prompt = f"""任务说明：{task}
参考示例：
{examples_text}
请参考以上示例格式完成任务。"""
        return self.clear_prompt(prompt)

# ===================== 演示方法：四大提示词原则调用示例 =====================
def prompt_principles_demo():
    """提示词设计原则示例演示 - 测试不同提示词的效果"""
    engineer = PromptEngineer()

    # 1. 清晰性原则示例：明确要求，精准回答
    clarity_response = engineer.generate_response(
        """请简要分析以下产品评价的情感倾向：
"这款手机拍照效果很棒，但是续航一般，总体来说还是很满意的。"
要求：
1. 给出情感倾向（积极/消极）
2. 列出关键词
3. 给出评分（1-5分）"""
    )

    # 2. 具体性原则示例：限定条件，精准生成
    specific_response = engineer.generate_response(
        """请为一款智能手表写一段50字以内的产品亮点描述。
要求：
- 突出续航和健康监测功能
- 使用简单易懂的语言
- 面向普通消费者"""
    )

    # 3. 上下文原则示例：补充背景，基于背景回答
    context_response = engineer.generate_response(
        """背景：一家初创公司正在开发在线教育产品
目标：提高小学生的学习兴趣
资源：AI技术、游戏化系统
请给出3点具体的产品功能建议。"""
    )

    # 封装结果打印方法
    def print_response(title, response):
        print(f"\n{title}")
        print("-" * 50)
        if response['status'] == 'success':
            print(response['content'].strip())
        else:
            print(f"Error: {response['message']}")

    # 打印三个示例的结果
    print_response("清晰性原则示例", clarity_response)
    print_response("具体性原则示例", specific_response)
    print_response("上下文原则示例", context_response)

# ===================== 程序入口 =====================
if __name__ == "__main__":
    prompt_principles_demo()