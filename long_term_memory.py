long_term_memory = {}

def save_memory(user_id, key, value):
    if user_id not in long_term_memory:
        long_term_memory[user_id] = {}
    long_term_memory[user_id][key] = value

def load_memory(user_id):
    return long_term_memory.get(user_id, {})
