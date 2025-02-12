import sys
import os
# ✅ Ensure the parent directory (IT_chatbot) is in Python’s path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def create_ticket(issue: str):
    """
    Creates an IT support ticket in Jira and SQLite.
    """

    # Create a ticket in Jira
    from chatbot.config import JIRA_CLIENT
    new_issue = JIRA_CLIENT.create_issue(
        project="IA",
        summary=issue,
        description="Automatically created by chatbot",
        issuetype={"name": "Task"}
    )    
    jira_ticket_id = new_issue.key
    from chatbot.database import add_tickets
    add_tickets(issue, jira_ticket_id)

    return {jira_ticket_id}

def get_ticket(ticket_id: str):
    """
    Retrieves the status of an IT support ticket.
    """
    from chatbot.database import get_ticket_status
    return get_ticket_status(ticket_id)
