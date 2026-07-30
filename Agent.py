from langchain_openai import ChatOpenAI
from state import MoneyState
from long_term_memory import load_memory, save_memory
from rag_search import rag_search

from langgraph.checkpoint import InMemorySaver
from langgraph.store import InMemoryStore
from langgraph.func import task, interrupt
from langgraph.types import RetryPolicy, Command

# -----------------------------
# 1) Checkpointer + Long-term Memory
# -----------------------------
checkpointer = InMemorySaver()
long_term_store = InMemoryStore()

# -----------------------------
# 2) LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------
# 3) Retry Policy
# -----------------------------
retry_policy = RetryPolicy(
    max_attempts=3,
    backoff_factor=2.0,
)

# -----------------------------
# 4) Main Agent Task (with retry)
# -----------------------------
@task(retry=retry_policy)
def main_agent(state: MoneyState) -> MoneyState:
    """
    Main financial assistant agent.
    Pattern: Prompt Chaining (analyze → recommend).
    Uses:
    - Long-term memory
    - RAG
    - Human-in-the-loop
    - Retry policy
    """

    user_message = state.query

    # Load long-term memory
    memory = load_memory("user1")

    # Retrieve RAG context
    context = rag_search(user_message)

    # Save user query to long-term memory (example)
    save_memory("user1", "last_query", user_message)

    # Human-in-the-loop: confirm large expenses
    if "صرف" in user_message or "مصروف" in user_message:
        decision = interrupt(
            "هل تريدين تأكيد تسجيل هذا المصروف؟ اكتبي yes أو no"
        )
        if decision.lower() != "yes":
            return Command(resume=state)

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

    try:
        response = llm.invoke(prompt)
    except Exception:
        # Fallback strategy
        response_content = "حدث خطأ أثناء التحليل. جربي إعادة صياغة السؤال."
    else:
        response_content = response.content

    # Append to conversation history
    state.messages.append({
        "role": "assistant",
        "content": response_content
    })

    return state

