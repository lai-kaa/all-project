import os
import requests
import base64
import json

# ===================== 配置区 - 修改这里即可 =====================
# 1. 【必填】填写你的 硅基流动 API密钥，复制粘贴到这里的引号中！！！
SILICON_API_KEY = "sk-clbegryjamknfhdpslmjcceokkokzdutkndolvqknwjskbib"
# 2. 绘图描述，可修改
PROMPT = "海边的岛屿，海鸥，月光照在海面上，灯塔，远处有船，鱼在海面上飞翔"
# 3. 其他配置，不用改
IMAGE_SIZE = "1024x1024"
SAVE_FILE_NAME = "silicon_http.png"
MODEL_NAME = "Kwai-Kolors/Kolors"


# ===================== 核心请求逻辑 =====================
def generate_image_by_silicon():
    # 固定接口地址，不用再读环境变量
    request_url = "https://api.siliconflow.cn/v1/images/generations"

    # 请求头 - 直接用硬编码的密钥，核心修改点！！！
    headers = {
        "Authorization": f"Bearer {SILICON_API_KEY}",  # 这里直接用写死的密钥
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "prompt": PROMPT,
        "image_size": IMAGE_SIZE,
        "response_format": "b64_json"
    }

    try:
        print(f"开始调用绘图API，描述内容：{PROMPT}")
        response = requests.post(
            url=request_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=120
        )
        response.raise_for_status()
        data = response.json()

        img_data = data["data"][0]
        with open(SAVE_FILE_NAME, "wb") as f:
            if "b64_json" in img_data:
                f.write(base64.b64decode(img_data["b64_json"]))
            elif img_url := img_data.get("url"):
                img_response = requests.get(img_url, timeout=120)
                img_response.raise_for_status()
                f.write(img_response.content)

        print(f"✅ 图片生成成功！已保存为: {SAVE_FILE_NAME}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {str(e)}")
    except json.JSONDecodeError:
        print(f"❌ 接口返回非JSON格式数据: {response.text}")
    except KeyError as e:
        print(f"❌ 返回数据格式异常，缺失字段: {str(e)}")
    except Exception as e:
        print(f"❌ 生成图片失败: {str(e)}")


if __name__ == "__main__":
    generate_image_by_silicon()