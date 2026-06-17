from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. 初始化本地模型 【核心修正：删掉模型名后面的空格】
llm = ChatOllama(model="gemma3:4b", temperature=0.9)

# 2. 定义冷笑话提示词模板
prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的冷笑话")

# 3. LCEL链式调用
chain = prompt | llm | StrOutputParser()

# 4. 调用并打印结果
result = chain.invoke({"topic": "程序员"})
print("✅ 冷笑话生成成功：\n", result)