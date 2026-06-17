import os
import requests
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量（本地密钥配置）
load_dotenv()


def test_http_api():
    """测试调用深度求索 DeepSeek 大模型 HTTP 接口"""
    # 接口地址
    url = "https://api.deepseek.com/chat/completions"
    # 请求头：携带API密钥 + 指定数据格式
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    # 请求体：大模型调用参数
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "用一句话解释 HTTP 请求。"}
        ],
        "stream": False  # 关闭流式输出，一次性返回完整结果
    }

    try:
        # 发送POST请求调用接口，超时时间30秒
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # 主动抛出HTTP状态码异常（4xx/5xx）

        # 解析返回的JSON数据并提取回答内容
        result = response.json()
        answer = result['choices'][0]['message']['content']
        print("=" * 50)
        print("✅ 大模型返回结果：\n", answer)
        print("=" * 50)

    except requests.exceptions.HTTPError as e:
        # 捕获HTTP错误（密钥错误、接口限流、参数错误等最常见）
        print(f"\n❌ HTTP请求错误: {e}")
        print(f"错误详情: {response.text}")
    except KeyError as e:
        # 捕获返回数据格式异常（字段缺失）
        print(f"\n❌ 解析返回数据失败: 缺失字段 {e}")
        print(f"原始返回数据: {response.json()}")
    except Exception as e:
        # 捕获其他所有异常（网络问题、超时等）
        print(f"\n❌ 请求失败: {str(e)}")


# 程序主入口
if __name__ == "__main__":
    test_http_api()