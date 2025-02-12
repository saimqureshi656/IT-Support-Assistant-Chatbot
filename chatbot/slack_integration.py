import sys
import os
# ✅ Ensure the parent directory (IT_chatbot) is in Python’s path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from slack_sdk.errors import SlackApiError
import requests


def notify_slack(issue, ticket_id):
    message = f"🚨 New IT Support Ticket 🚨\nIssue: {issue}\nTicket ID: {ticket_id}"
    from chatbot.config import SLACK_WEBHOOK_URL
    requests.post (SLACK_WEBHOOK_URL, json= {"text": message})

def escalate_to_slack(issue: str):
   try:
      from chatbot.config import SLACK_CHANNEL, SLACK_CLIENT
      SLACK_CLIENT.chat_postMessage(channel = SLACK_CHANNEL, text=f"🚨 IT Support Alert: {issue}")
      return {"message": "Issue escalated to IT support on Slack"}
   except SlackApiError as e:
      return {"error": str(e)}


