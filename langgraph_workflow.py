graph = StateGraph(MoneyState)

graph.add_node("main_agent", main_agent)
graph.set_entry_point("main_agent")
graph.add_edge("main_agent", END)

app = graph.compile()
