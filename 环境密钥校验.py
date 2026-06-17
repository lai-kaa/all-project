from dotenv import load_dotenv
import os, sys
load_dotenv()
required = ["DEEPSEEK_API_KEY","DEEPSEEK_BASE_URL"]
missing = [k for k in required if not os.getenv(k)]
if missing:
 print(",".join(missing))
 sys.exit(1)