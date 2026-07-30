def rag_search(query):
    results = vector_store.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])
