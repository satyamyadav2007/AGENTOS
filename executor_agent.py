from tools import web_search, weather, crypto, read_file

def execute_step(step: str):
    if "weather" in step.lower():
        return weather("Delhi")
    if "crypto" in step.lower():
        return crypto("bitcoin")
    if "file" in step.lower():
        return read_file("data.txt")

    return web_search(step)