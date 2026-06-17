import os
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
class Resume(BaseModel):
 name: str = Field(description="候选人姓名")
 skills: List[str] = Field(description="技能列表，字符串数组")
 role: str = Field(description="目标岗位")
load_dotenv()
parser = PydanticOutputParser(pydantic_object=Resume)
prompt = ChatPromptTemplate.from_messages([
 ("system","从输入中抽取 name, skills, role。严格按给定格式输出。"),
 ("system","{format_instructions}"),
 ("human","{text}")
])
model = ChatOpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
base_url=os.getenv("DEEPSEEK_BASE_URL"), model="deepseek-chat")
chain = prompt | model | parser
data = chain.invoke({
 "text":"我叫李雷，擅长Python、LangChain、RAG，想做数据工程师",
 "format_instructions": parser.get_format_instructions()
})
print(data.model_dump_json(ensure_ascii=False))