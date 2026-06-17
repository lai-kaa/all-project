import os
from openai import OpenAI
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def generate_image(prompt: str, model: str = "dall-e-3", size: str = "1024x1024"):
    client = OpenAI(
        api_key=os.getenv('SILICON_API_KEY'),
        base_url=os.getenv('SILICON_BASE_URL', 'https://api.siliconflow.cn/v1')
    )
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        n=1,
        quality="standard",
        response_format="url"
    )
    return response.data[0].url if response and response.data else None


def save_image(url: str, save_path: str = "generated_image.png"):
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"图像已保存至: {save_path}")


if __name__ == "__main__":
    # 示例使用
    image_url = generate_image(
        prompt="海边的岛屿，有海鸥，月光洒在海面上，灯塔，背景有船，鱼在海面上飞翔",
        model="Kwai-Kolors/Kolors",
        size="1024x1024"
    )

    if image_url:
        save_image(image_url, "ocean_scene.png")
