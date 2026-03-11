import time

def log(agent, task, start_time):
    duration = time.time() - start_time
    print(f"[LOG] {agent} | {task} | {duration:.2f}s")