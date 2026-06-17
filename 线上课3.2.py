import os
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings


# ========== 定义模型1：基础关键词嵌入模型 ==========
class BasicKeywordEmbeddings(Embeddings):
    """基础版关键词嵌入模型，关键词出现则对应维度为1"""

    def __init__(self):
        self.keyword_map = {
            "小明": 0,
            "生日": 1,
            "密码": 2,
            "公司": 3,
            "天气": 4,
            "北京": 5,
            "产品": 6,
            "上线": 7,
            "DeepSeek": 8,
            "模型": 9
        }

    def embed_documents(self, texts):
        return [self._text_to_vector(text) for text in texts]

    def embed_query(self, text):
        return self._text_to_vector(text)

    def _text_to_vector(self, text):
        vector = [0.0] * 10
        for keyword, idx in self.keyword_map.items():
            if keyword in text:
                vector[idx] = 1.0
        return vector


# ========== 定义模型2：加权关键词嵌入模型 ==========
class WeightedKeywordEmbeddings(Embeddings):
    """加权版关键词嵌入模型，核心关键词权重更高"""

    def __init__(self):
        self.keyword_map = {
            "小明": (0, 1.0),  # (维度, 权重)
            "生日": (1, 1.0),
            "密码": (2, 1.5),  # 核心信息权重提升
            "公司": (3, 1.0),
            "天气": (4, 1.0),
            "北京": (5, 1.5),  # 地点关键词权重提升
            "产品": (6, 1.0),
            "上线": (7, 1.0),
            "DeepSeek": (8, 2.0),  # 品牌关键词权重最高
            "模型": (9, 1.0)
        }

    def embed_documents(self, texts):
        return [self._text_to_vector(text) for text in texts]

    def embed_query(self, text):
        return self._text_to_vector(text)

    def _text_to_vector(self, text):
        vector = [0.0] * 10
        for keyword, (idx, weight) in self.keyword_map.items():
            if keyword in text:
                vector[idx] = weight
        return vector


# ========== 准备实验数据 ==========
texts = [
    "小明的生日是10月1日",
    "公司的Wifi密码是12345678",
    "产品上线时间是2026年3月15日",
    "北京今天天气晴，温度25°C",
    "DeepSeek-R1是一个开源商用的大模型"
]

# ========== 构建两个向量库 ==========
# 模型1 向量库
embedding_basic = BasicKeywordEmbeddings()
vector_store_basic = Chroma.from_texts(
    texts,
    embedding_basic,
    persist_directory="./chroma_db_basic",
    collection_name="basic_memory"
)

# 模型2 向量库
embedding_weighted = WeightedKeywordEmbeddings()
vector_store_weighted = Chroma.from_texts(
    texts,
    embedding_weighted,
    persist_directory="./chroma_db_weighted",
    collection_name="weighted_memory"
)


# ========== 定义对比检索函数 ==========
def compare_models(query, top_k=3):
    print(f"===== 查询问题：{query} =====")

    # 模型1 检索结果
    results_basic = vector_store_basic.similarity_search_with_score(query, k=top_k)
    print("【模型1：基础关键词嵌入模型 结果】")
    for doc, score in results_basic:
        print(f"文本: {doc.page_content}")
        print(f"相似度距离分数: {score:.4f}")
        print("-" * 30)

    # 模型2 检索结果
    results_weighted = vector_store_weighted.similarity_search_with_score(query, k=top_k)
    print("\n【模型2：加权关键词嵌入模型 结果】")
    for doc, score in results_weighted:
        print(f"文本: {doc.page_content}")
        print(f"相似度距离分数: {score:.4f}")
        print("-" * 30)
    print("=" * 60 + "\n")


# ========== 执行对比查询 ==========
if __name__ == "__main__":
    # 设计3个查询问题
    queries = [
        "小明的生日是哪天？",
        "公司的网络密码是什么？",
        "DeepSeek是什么类型的模型？"
    ]
    for q in queries:
        compare_models(q)