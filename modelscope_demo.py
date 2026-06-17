from modelscope import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. 下载模型（已经下载完成，会直接读取本地缓存，不会重复下载）
model_dir = snapshot_download("Qwen/Qwen2.5-0.5B-Instruct")

# 2. 加载模型与分词器 → 删掉所有报错的参数，只保留核心必写项
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    trust_remote_code=True  # 只保留这一个核心参数，其余全部删掉
)

# 3. 推理（不变，你的原代码）
prompt = "你好，请介绍一下你自己。"
inputs = tokenizer(prompt, return_tensors="pt")
pred = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))