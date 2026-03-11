from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="mistral", temperature=0.2)

def plan_task(task: str):
    prompt = f"""
You are a task planner AI.

User Task:
{task}

Break this task into clear numbered steps.
Only output steps.
"""
    return llm.invoke(prompt).content