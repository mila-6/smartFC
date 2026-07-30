---
# smartFC

smartFC is an AI-powered financial assistant designed to help users manage their money more effectively, avoid overspending, and improve their financial planning. The system provides budgeting guidance, expense analysis, and personalized recommendations using LangGraph workflows and a RAG-enhanced LLM pipeline.

## Workflow pattern

Workflow pattern: Orchestrator-Worker. The orchestrator invokes a worker task (`main_agent`) that performs the main LLM work; the orchestrator handles retries and checkpointing.

## RAG strategy

RAG strategy: 2‑Step RAG (retrieval → answer). We run a retrieval pass (FAISS + Embeddings) to get the top-k supporting documents, then pass these as context to the model to generate grounded answers. This approach keeps the pipeline simple and reliable for a small domain of concise financial guidance and avoids the complexity of agentic/hybrid RAG.

## Training Programme

**Programme Name:** Building AI Agents  
**Dates:** 26/07/2026 – 30/07/2026

This project was completed as part of the "Building AI Agents" training programme, focusing on constructing intelligent agents using LangGraph, LangChain, and related AI tooling.

## Run instructions

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit UI:

   ```bash
   streamlit run ui.py
   ```

The UI imports `app` and `MoneyState` from `main.py`. The LangGraph entrypoint `app` wraps the workflow and injects a process-lifetime `InMemoryStore` for long-term memory.

## SDAIA Academy

GitHub: https://github.com/SDAIAAcademy

## About (suggested repo description)

SmartFC — small LangGraph + LangChain demo: a Streamlit financial assistant using a 2‑step RAG pipeline and LangGraph workflows.
