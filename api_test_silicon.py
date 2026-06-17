import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 加载项目根目录的.env环境变量文件
load_dotenv()

def test_langchain_api():
    """
    使用 LangChain 框架调用 DeepSeek 大模型 (基于LCEL标准链式调用)
    LangChain 兼容 OpenAI 生态，可无缝对接DeepSeek等兼容型大模型
    """
    # 1. 配置DeepSeek密钥/地址/模型参数
    llm = ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        model="deepseek-chat",
        temperature=0.7,  # 0-1，值越大回答越随机，越小越精准
        timeout=30         # 新增超时配置，防止请求卡死
    )

    # 2. 定义提示词模板 - 标准化对话格式
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个技术专家。"),
        ("user", "{input}")
    ])

    # 3. 构建LCEL标准调用链 (核心语法)
    # LCEL语法：| 管道符 依次执行 提示词渲染 -> 模型调用 -> 结果解析
    chain = prompt | llm | StrOutputParser()

    # 4. 执行调用并返回结果
    try:
        result = chain.invoke({"input": "用一句话解释 LangChain LCEL。"})
        # 美化输出结果
        print("=" * 70)
        print("✅ LangChain 调用成功 ↓")
        print(result)
        print("=" * 70)
    except Exception as e:
        print("=" * 70)
        print(f"❌ LangChain 调用失败: {str(e)}")
        print("=" * 70)

# 程序主入口
if __name__ == "__main__":
    test_langchain_api()