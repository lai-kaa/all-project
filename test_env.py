import sys
import importlib

# 核心依赖库列表
LIBS = [
    "langchain",
    "langchain_community",
    "langchain_openai",
    "langgraph",
    "openai",
    "requests",
    "python_dotenv",
    "streamlit",
    "pydantic",
    "modelscope",
    "chromadb",
    "faiss-cpu",  # 安装包名
    "tiktoken",
    "sentence_transformers",
    "pypdf",
    "sqlalchemy",
    "pandas",
    "mcp",
    "tavily",
    "langchain_deepseek",
]


def get_version(module):
    """获取模块版本号"""
    for attr in ("__version__", "VERSION", "version"):
        v = getattr(module, attr, None)
        if isinstance(v, str):
            return v
    return "installed"


def test_environment():
    print(f"Python版本: {sys.version}")
    print("-" * 30)
    all_passed = True

    for name in LIBS:
        try:
            # ========== 核心修复：新增 faiss-cpu 的导入名映射 ==========
            if name == "python_dotenv":
                import_name = "dotenv"
            elif name == "faiss-cpu":
                import_name = "faiss"
            else:
                import_name = name

            module = importlib.import_module(import_name)
            print(f"[√] {name:<25}: {get_version(module)}")
        except Exception as e:
            print(f"[×] {name:<25}: 未安装或导入失败 -> {e}")
            all_passed = False

    if all_passed:
        print("🎉 环境验证成功！所有依赖均已就绪。")
    else:
        print("⚠ 环境验证未通过，请检查上述报错模块。")


if __name__ == "__main__":
    test_environment()