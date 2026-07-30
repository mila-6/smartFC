from pydantic import BaseModel
from typing import List, Dict, Any

class MoneyState(BaseModel):
    """
    State object used by the LangGraph Functional API.
    Holds the user query, messages, and memory.
    """
    query: str
    messages: List[Dict[str, Any]] = []
    memory: Dict[str, Any] = {}
    output: str | None = None
