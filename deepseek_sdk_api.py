import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载项目根目录下的 .env 环境变量文件
load_dotenv()

def test_sdk_api():
    """
    使用 OpenAI 兼容的 SDK 方式调用 DeepSeek 大模型
    DeepSeek 兼容 OpenAI 的 SDK 调用规范，无需额外安装SDK，直接用openai库即可
    """
    # 初始化大模型客户端
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),  # 从环境变量读取API密钥
        base_url=os.getenv("DEEPSEEK_BASE_URL") # 从环境变量读取DeepSeek的API基准地址
    )

    try:
        # 调用大模型对话接口
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "用一句话解释 SDK 的作用。"}
            ],
            stream=False  # 关闭流式返回，一次性获取完整结果
        )
        # 打印返回结果
        print("=" * 60)
        print("✅ SDK调用成功 | 大模型回答：")
        print(response.choices[0].message.content)
        print("=" * 60)

    except Exception as e:
        print("=" * 60)
        print(f"❌ SDK 调用失败: {str(e)}")
        print("=" * 60)

# 程序主入口
if __name__ == "__main__":
    test_sdk_api()