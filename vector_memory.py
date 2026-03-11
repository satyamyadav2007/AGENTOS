import operator
from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize Vector Database
db = FAISS.from_texts(["AgentOS initialized"], embeddings)

def store(text):
    db.add_texts([text])

def search(query):
    docs = db.similarity_search(query, k=3)
    return "\n".join(d.page_content for d in docs)

# NOTE: This class usually belongs in agent_runtime.py, not here.
# If you are sure you want it here, this is the correct syntax:
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    query: str