financial_docs = [
    "الادخار المثالي يكون بين 10% إلى 30% من الدخل.",
    "تتبع المصاريف يساعد في تحسين القرارات المالية.",
    "تقسيم الميزانية إلى ثابتة ومتغيرة يساعد في التحكم بالصرف."
]

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_texts(financial_docs, embeddings)
