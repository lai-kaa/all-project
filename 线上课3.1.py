import os
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings


class SemanticMockEmbeddings(Embeddings):
    """基于关键词的语义感知模拟嵌入模型"""

    def __init__(self):
        # 定义关键词到向量维度的映射
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
        # 初始化一个10维的零向量
        vector = [0.0] * 10
        # 对文本中的关键词进行加权
        for keyword, idx in self.keyword_map.items():
            if keyword in text:
                vector[idx] = 1.0  # 关键词出现则对应维度设为1
        return vector


# 初始化语义感知的模拟嵌入模型
embedding_model = SemanticMockEmbeddings()

# 准备中文文本数据
texts = [
    "小明的生日是10月1日",
    "公司的Wifi密码是12345678",
    "产品上线时间是2026年3月15日",
    "北京今天天气晴，温度25°C",
    "DeepSeek-R1是一个开源商用的大模型"
]

# 构建向量库
vector_store = Chroma.from_texts(
    texts,
    embedding_model,
    persist_directory="./chroma_db",
    collection_name="local_memory"
)


# 相似性检索函数
def search_similar(query, top_k=3):
    results = vector_store.similarity_search_with_score(query, k=top_k)
    print(f"查询问题：{query}")
    print("=" * 60)
    for doc, score in results:
        print(f"文本: {doc.page_content}")
        print(f"相似度分数（距离越小越相似）: {score:.4f}")
        print("-" * 50)
    return results


# 测试检索
if __name__ == "__main__":
    search_similar("小明的生日是哪天？")
    search_similar("公司的网络密码是什么？")