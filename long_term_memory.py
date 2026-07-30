# Simple in-memory long-term memory store

long_term_memory = {}

def save_memory(user_id: str, key: str, value):
    """
    Save a memory value for a specific user.
    """
    if user_id not in long_term_memory:
        long_term_memory[user_id] = {}
    long_term_memory[user_id][key] = value

def load_memory(user_id: str):
    """
    Load all memory for a specific user.
    Returns an empty dictionary if the user has no stored memory.
    """
    return long_term_memory.get(user_id, {})
