import sqlite3
from jira import JIRA
# connect to sqlite database
conn = sqlite3.connect("tickets.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table for Tickets
cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jira_ticket_id TEXT UNIQUE,             
    issue TEXT,
    status TEXT)''')
conn.commit()

def update_ticket_status(ticket_id: str, new_status: str):
    """
    Updates the status of a ticket in the database.
    """
    cursor.execute("UPDATE tickets SET status=? WHERE jira_ticket_id=?", (new_status, ticket_id))
    conn.commit()

def add_tickets(issue : str, jira_ticket_id : str):

    cursor.execute("INSERT INTO tickets (jira_ticket_id, issue, status) VALUES (?, ?, ?)", 
                   (jira_ticket_id, issue, "Open"))
    conn.commit()
    return jira_ticket_id #retunr the ticket ID

def get_ticket_status(ticket_id: str):
    #fetch ticket status from jira
    JIRA_SERVER = "https://saimqureshi656.atlassian.net"
    JIRA_USER = "saimqureshi656@gmail.com"
    JIRA_API_TOKEN = "ATATT3xFfGF0FrXEvqgTca0DbDztRXFHdJ9QZWIV9UT8FcqovTr1RcDKOSEsXOH7FR58ewRl9blGqdlQCHTXcr4NJhcWBmtXARThI48AGbCkSDtT2lzqss02rr2SVDqYA7U5qTKI9ayHOALA40wbghFT8QBF38nS4qmNtzWbsS0OAl7L5wJy-5Y=75C5DA42"
    JIRA_CLIENT = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

    try:
        jira_issue = JIRA_CLIENT.issue(ticket_id)
        latest_status = jira_issue.fields.status.name  # Get latest Jira status
    except Exception as e:
        return {"error": f"Ticket not found"}

    cursor.execute("SELECT status FROM tickets WHERE jira_ticket_id=?", (ticket_id,))
    ticket = cursor.fetchone()

    if ticket:
        db_status = ticket[0]

        if db_status!=latest_status:
            update_ticket_status(ticket_id, latest_status)

        return {latest_status}
    return {"error": "Ticket not found in database."}