import sys
import os

# ✅ Ensure the parent directory (IT_chatbot) is in Python’s path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Chatbot API is working with all modules!"}

@app.get("/chat")
def chat(query: str):
    from chatbot.knowledge_base import chatbot_response
    response = chatbot_response(query, first_message=False)
    return {"query": query, "response": response["response"]}

@app.post("/create_ticket")
def create(issue: str):
    from chatbot import create_ticket
    return create_ticket(issue)

@app.get("/get_ticket")
def get_status(ticket_id: str):
    from chatbot import create_ticket, get_ticket
    return get_ticket(ticket_id)

@app.post("/escalate_to_slack")
def escalate(issue: str):
    from chatbot.slack_integration import escalate_to_slack
    return escalate_to_slack(issue)
