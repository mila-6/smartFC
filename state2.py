state = MoneyState(messages=[], memory={}, query="كيف أنظم مصاريفي؟")

result = app.invoke(state)
print(result.messages[-1]["content"])

