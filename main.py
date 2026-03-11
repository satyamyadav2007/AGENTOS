from fastapi import FastAPI
from pydantic import BaseModel
from agent_runtime import agent_app  # <--- Importing the NEW brain

app = FastAPI()

# Data model matching what the frontend sends
class Request(BaseModel):
    task: str
    user_id: str = "Admin"

@app.post("/run")
def run_agent(req: Request):
    print(f"📨 Request received: {req.task}")
    
    # Run the LangGraph agent
    # We pass 'task' which matches the AgentState definition
    result = agent_app.invoke({"task": req.task, "user_id": req.user_id})
    
    # Return the result
    return result