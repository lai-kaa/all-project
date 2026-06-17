import requests
import json
import time
import os
import sys
import pkg_resources

# ==================== 全局配置 ====================
# 请替换为你的实际API密钥
API_KEY = "your_deepseek_api_key"
BASE_URL = "https://api.deepseek.com/v1/chat/completions"
IMAGE_API_URL = "https://api.deepseek.com/v1/images/generations"

# ==================== 任务1：模型调用与回复对比 ====================
def call_deepseek_model(prompt, model_name):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(BASE_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# 定义提示词
prompt_a = """已知一个四位数，其千位数字是百位数字的平方，十位数字比个位数字小5，且该数本身是37的倍数。若该数的各位数字均为质数（允许重复），求所有可能解。"""
prompt_b = """甲说：‘如果乙说了真话，则丙在说谎。’乙说：‘如果丙说了真话，则甲在说谎。’丙说：‘我们三人中至少两人说谎。’已知只有一人说真话，且说真话者的陈述为真，其余陈述均为假。请确定谁说了真话。"""

# 调用两个模型并对比结果
def run_task1():
    print("="*50 + " 任务1 模型回复对比 " + "="*50)
    models = ["deepseek-chat", "deepseek-reasoner"]
    results_task1 = {}
    for model in models:
        res_a = call_deepseek_model(prompt_a, model)
        res_b = call_deepseek_model(prompt_b, model)
        results_task1[model] = {"prompt_a": res_a, "prompt_b": res_b}

    # 打印结果
    for model, res in results_task1.items():
        print(f"\n===== {model} =====")
        print(f"Prompt a 回复: {res['prompt_a']}")
        print(f"\nPrompt b 回复: {res['prompt_b']}")

# ==================== 任务2：流式输出改造 ====================
def stream_deepseek_model(prompt, model_name):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": True
    }
    response = requests.post(BASE_URL, headers=headers, json=data, stream=True)
    print(f"\n===== 流式输出 - {model_name} =====")
    for chunk in response.iter_lines():
        if chunk:
            chunk = chunk.decode("utf-8").replace("data: ", "")
            if chunk != "[DONE]":
                try:
                    content = json.loads(chunk)["choices"][0]["delta"].get("content", "")
                    print(content, end="", flush=True)
                except:
                    pass
    print("\n")

def run_task2():
    print("\n" + "="*50 + " 任务2 流式输出 " + "="*50)
    stream_deepseek_model(prompt_a, "deepseek-chat")
    stream_deepseek_model(prompt_b, "deepseek-reasoner")

# ==================== 任务3：基础图像生成 ====================
def generate_image(prompt, save_path):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    start_time = time.time()
    response = requests.post(IMAGE_API_URL, headers=headers, json=data)
    end_time = time.time()
    cost_time = round(end_time - start_time, 2)

    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        img_response = requests.get(image_url)
        with open(save_path, "wb") as f:
            f.write(img_response.content)
        return True, cost_time
    else:
        return False, cost_time

def run_task3():
    print("\n" + "="*50 + " 任务3 图像生成 " + "="*50)
    # 图像生成提示词
    image_prompts = {
        "a": "圆形红色logo，白色背景",
        "b": "卡通风格太阳笑脸",
        "c": "黑白条纹的斑马",
        "d": "由三角形组成的山脉"
    }

    # 创建保存目录
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")

    # 生成图像并记录耗时
    image_results = []
    for key, prompt in image_prompts.items():
        save_path = f"generated_images/image_{key}.png"
        success, cost = generate_image(prompt, save_path)
        status = "成功" if success else "失败"
        image_results.append(
            {"提示词编号": key, "提示词内容": prompt, "保存路径": save_path, "耗时(s)": cost, "状态": status})

    # 输出生成结果统计表
    print("\n===== 图像生成结果统计表 =====")
    print(f"{'编号':<5}{'提示词':<30}{'保存路径':<30}{'耗时(s)':<10}{'状态':<5}")
    for res in image_results:
        print(f"{res['提示词编号']:<5}{res['提示词内容']:<30}{res['保存路径']:<30}{res['耗时(s)']:<10}{res['状态']:<5}")

# ==================== 任务4：环境配置验证 ====================
# a) 验证API密钥有效性
def check_api_key():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(BASE_URL, headers=headers,
                             json={"model": "deepseek-chat", "messages": [{"role": "user", "content": "test"}]})
    return response.status_code == 200

# b) 测试API服务连通性
def check_service_connectivity():
    try:
        response = requests.get("https://api.deepseek.com/v1/models")
        return response.status_code == 200
    except:
        return False

# c) 获取可用模型列表
def get_available_models():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get("https://api.deepseek.com/v1/models", headers=headers)
    if response.status_code == 200:
        return [model["id"] for model in response.json()["data"]]
    else:
        return ["获取失败"]

# d) 打印环境配置信息
def get_env_info():
    python_version = sys.version.split()[0]
    libs = ["requests", "python-docx"]
    lib_versions = {}
    for lib in libs:
        try:
            lib_versions[lib] = pkg_resources.get_distribution(lib).version
        except:
            lib_versions[lib] = "未安装"
    return python_version, lib_versions

def run_task4():
    print("\n" + "="*50 + " 任务4 环境配置验证 " + "="*50)
    # 执行验证
    api_valid = check_api_key()
    service_ok = check_service_connectivity()
    models_list = get_available_models()
    python_ver, lib_vers = get_env_info()

    # 输出结果
    print(f"[{'✓' if api_valid else '✗'}] API密钥验证通过")
    print(f"[{'✓' if service_ok else '✗'}] 服务端连接正常")
    print(f"可用模型: {', '.join(models_list)}")
    print(f"Python版本: {python_ver}")
    print("库版本信息:")
    for lib, ver in lib_vers.items():
        print(f"  - {lib}: {ver}")

# ==================== 主函数：执行所有任务 ====================
if __name__ == "__main__":
    run_task1()
    run_task2()
    run_task3()
    run_task4()
    print("\n" + "="*50 + " 所有任务执行完毕 " + "="*50)