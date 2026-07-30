llm = ChatOpenAI(model="gpt-4o-mini")

def main_agent(state: MoneyState):
    user_message = state.query
    memory = load_memory("user1")

    context = rag_search(user_message)

    response = llm([
        HumanMessage(content=f"""
        أنت مساعد مالي ذكي.
        ذاكرة المستخدم: {memory}
        سياق RAG:
        {context}

        سؤال المستخدم:
        {user_message}

        رد بشكل واضح ومنظم.
        """)
    ])

    state.messages.append({"role": "assistant", "content": response.content})
    return state
