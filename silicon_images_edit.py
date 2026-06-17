import os
import base64
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 构建API URL
base_url = os.getenv("SILICON_BASE_URL",
                     os.getenv("SILICON_API_BASE_URL", "https://api.siliconflow.cn/v1"))
url = f"{base_url}/images/generations"

# 设置请求头
headers = {
    "Authorization": f"Bearer {os.getenv('SILICON_API_KEY', '')}",
    "Content-Type": "application/json",
}

# 请求负载
payload = {
    "model": "Qwen/Qwen-Image-Edit-2509",
    "prompt": "在原图基础上增加灯塔与月光效果",
    "image": "https://inews.gtimg.com/om_bt/Os3eJ8u3SgB3Kd-zrRRhgfR5hUvdwcVPKUTNO6O7sZfUwAA/641",
    "image_size": "1024x1024",
    "num_inference_steps": 20,
    "response_format": "b64_json"
}

try:
    # 发送POST请求
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    r.raise_for_status()  # 检查请求是否成功

    # 解析响应
    data = r.json()

    # 根据API响应结构调整
    if "data" in data and len(data["data"]) > 0:
        item = data["data"][0]
    else:
        # 有些API可能直接返回数据而不是嵌套在data字段中
        item = data

    # 保存图片
    out = "silicon_edit.png"

    if "b64_json" in item:
        with open(out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
    elif "url" in item:
        resp = requests.get(item.get("url"), timeout=120)
        resp.raise_for_status()
        with open(out, "wb") as f:
            f.write(resp.content)
    else:
        print("API响应中没有找到图片数据")
        print("完整响应:", json.dumps(data, indent=2, ensure_ascii=False))

    print(f"图片已保存为: {out}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
    if 'r' in locals():
        print(f"响应状态码: {r.status_code}")
        print(f"响应内容: {r.text}")
except KeyError as e:
    print(f"解析响应时出错，缺少字段: {e}")
    print(f"完整响应: {data}")
except Exception as e:
    print(f"发生未知错误: {e}")