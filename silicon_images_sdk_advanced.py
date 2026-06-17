import os
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量(.env文件)，读取密钥和接口地址
load_dotenv()

# 初始化OpenAI兼容的客户端 (核心：硅基流动完全兼容OpenAI的SDK)
client = OpenAI(
    api_key=os.getenv("SILICON_API_KEY", ""),
    base_url=os.getenv(
        "SILICON_BASE_URL",
        os.getenv("SILICON_API_BASE_URL", "https://api.siliconflow.cn/v1")
    )
)

# 核心绘图配置 - 按需修改即可
prompt_text = "未来城市夜景，霓虹灯与悬浮车辆，赛博朋克风格，8K高清，光影绚丽，细节丰富"
model_name = "Kwai-Kolors/Kolors"
img_size = "1024x1024"
img_num = 2  # 生成图片的数量

try:
    # 调用文生图API
    print(f"开始生成 {img_num} 张图片，描述：{prompt_text}")
    resp = client.images.generate(
        model=model_name,
        prompt=prompt_text,
        size=img_size,
        n=img_num,
        response_format="b64_json",  # 优先返回Base64格式，无需二次下载
    )

    # 遍历生成的每张图片，逐个保存
    for i, item in enumerate(resp.data):
        save_name = f"silicon_sdk_{i}.png"
        # 方式1：Base64格式解码保存 (推荐，速度更快)
        if getattr(item, "b64_json", None):
            with open(save_name, "wb") as f:
                f.write(base64.b64decode(item.b64_json))
            print(f"✅ 图片保存成功：{save_name}")
        # 方式2：兼容URL格式下载保存
        elif getattr(item, "url", None):
            r = requests.get(item.url, timeout=120)
            r.raise_for_status()
            with open(save_name, "wb") as f:
                f.write(r.content)
            print(f"✅ 图片下载保存成功：{save_name}")

    print("\n🎉 全部图片生成完成！")

except Exception as e:
    print(f"\n❌ 图片生成失败：{str(e)}")