from langchain_openai import ChatOpenAI
from state import MoneyState
from long_term_memory import load_memory
from rag_search import rag_search

# Your LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def main_agent(state: MoneyState) -> MoneyState:
    """
    Main financial assistant agent.
    Uses memory + RAG + LLM to produce a structured response.
    """

    user_message = state.query

    # Load long-term memory
    memory = load_memory("user1")

    # Retrieve RAG context
    context = rag_search(user_message)

    # Build the prompt
    prompt = f"""
    أنت مساعد مالي ذكي.
    
    ذاكرة المستخدم:
    {memory}

    سياق RAG:
    {context}

    سؤال المستخدم:
    {user_message}

    رد بشكل واضح ومنظم.
    """

    # Call the LLM
    response = llm.invoke(prompt)

    # Append to conversation history
    state.messages.append({
        "role": "assistant",
        "content": response.content
    })

    return state

