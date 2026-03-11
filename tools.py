from duckduckgo_search import DDGS
import requests
import os

class AgentTools:
    @staticmethod
    def read_emails():
        return ["Email 1", "Email 2"]
    

def web_search(query):
    results = []
    
    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=5)
        
        for r in search_results:
            results.append({
                "title": r["title"],
                "link": r["href"],
                "snippet": r["body"]
            })

    return results

def weather(city):
    return f"Weather in {city}: 25°C (mock free)"

def crypto(symbol):
    return f"{symbol.upper()} price: $42000 (mock)"

def read_file(path):
    with open(path, "r", errors="ignore") as f:
        return f.read()[:2000]