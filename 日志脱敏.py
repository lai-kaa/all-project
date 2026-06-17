import os
def redact(s):
 return s[:4] + "..." + s[-4:] if s and len(s)>8 else "***"
print(redact(os.getenv("DEEPSEEK_API_KEY","")))