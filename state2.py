state = MoneyState(messages=[], memory={}, query="كيف أنظم مصاريفي؟")

result = app.invoke(state)
result.messages[-1]["content"]
