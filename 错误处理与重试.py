import os, time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def safe_request(prompt, max_retries=3):
    wait = 2
    for _ in range(max_retries):
        try:
            r = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role":"user","content":prompt}]
            )
            return {"status":"success","content":r.choices[0].message.content}
        except Exception as e:
            msg = str(e).lower()
            if "authentication" in msg or "invalid request" in msg:
                return {"status":"error","error":msg}
            time.sleep(wait)
            wait *= 2
    return {"status":"error","error":"max_retries"}