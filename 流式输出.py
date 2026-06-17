import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
base_url=os.getenv("DEEPSEEK_BASE_URL"))
stream = client.chat.completions.create(
 model="deepseek-chat",
 messages=[{"role":"user","content":"演示流式输出"}],
 stream=True,
)
buf = ""
for chunk in stream:
 delta = chunk.choices[0].delta.content or ""
 print(delta, end="", flush=True)
 buf += delta
print()
print(buf)