from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from os_kernel import MemoryManager, PermissionEngine
from vector_memory import store, search
import time

# ---------------- LLM (Brain) ----------------
# We use TinyLlama because it fits on your laptop
llm = ChatOllama(
    model="tinyllama",
    temperature=0.2,
    num_ctx=2048
)

# ---------------- Tools ----------------
web_search_tool = DuckDuckGoSearchRun() 
memory = MemoryManager()
permissions = PermissionEngine()

# ---------------- State ----------------
# FIX: We use 'total=False' so keys are optional (prevents KeyErrors)
class AgentState(TypedDict, total=False):
    task: str       # <--- Added this
    query: str      # <--- Kept this for safety
    user_id: str    # <--- Added this
    user: str       # <--- Kept this
    response: str
    output: str     # <--- Added for frontend compatibility
    messages: Annotated[List[BaseMessage], operator.add]

# ---------------- Nodes ----------------
def supervisor(state: AgentState):
    return state

def executor(state: AgentState):
    # FIX: Check for 'task' OR 'query' so it never crashes
    q = state.get("task") or state.get("query")
    
    # FIX: Check for 'user_id' OR 'user'
    user = state.get("user_id") or state.get("user") or "Admin"
    
    print(f"🤖 [Executor] Processing for {user}: {q}")

    # --- 1. Clean Web Search ---
    try:
        if q:
            web_data = web_search_tool.invoke(q)
        else:
            web_data = "No query provided."
    except Exception as e:
        web_data = "Internet search unavailable."

    # --- 2. Check Memory ---
    vec_mem = search(q) if q else ""

    # --- 3. Build Prompt ---
    prompt = f"""
    You are a helpful AI assistant.
    
    User Question: {q}
    
    Search Results:
    {web_data}
    
    Answer the user's question using the Search Results. Keep it short.
    """

    # --- 4. Get Answer ---
    ai_msg = llm.invoke(prompt)
    response_text = ai_msg.content

    # --- 5. Save & Return ---
    memory.save(user, response_text)
    store(response_text)

    # FIX: Return both 'response' and 'output' to satisfy any frontend
    return {
        "response": response_text, 
        "output": response_text
    }

# ---------------- Graph ----------------
graph = StateGraph(AgentState)

graph.add_node("supervisor", supervisor)
graph.add_node("executor", executor)

graph.set_entry_point("supervisor")
graph.add_edge("supervisor", "executor")
graph.add_edge("executor", END)

agent_app = graph.compile()