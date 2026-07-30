from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# -----------------------------------------
# RAG Strategy Justification
# -----------------------------------------
# نستخدم RAG من خطوتين (2-Step RAG):
# 1) استرجاع النصوص المالية الأقرب للسؤال باستخدام FAISS + Embeddings.
# 2) تمرير النصوص المسترجعة للنموذج لبناء إجابة مدعومة بالمحتوى.
#
# هذا مناسب لأن نطاق المعرفة محدود (نصوص مالية قصيرة)،
# ولا نحتاج تعقيد Agentic أو Hybrid RAG.
# التركيز هنا على استرجاع دقيق + إجابة واضحة.
# -----------------------------------------

financial_docs = [
    "الادخار المثالي يكون بين 10% إلى 30% من الدخل.",
    "تتبع المصاريف يساعد في تحسين القرارات المالية.",
    "تقسيم الميزانية إلى ثابتة ومتغيرة يساعد في التحكم بالصرف."
]

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_texts(financial_docs, embeddings)

def rag_search(query: str) -> str:
    """
    Perform a simple RAG search over financial_docs.
    """
    results = vector_store.similarity_search(query, k=2)
    return "\n".join([doc.page_content for doc in results])
