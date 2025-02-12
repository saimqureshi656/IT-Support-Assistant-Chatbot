import re
import sys
import os
# ✅ Ensure the parent directory (IT_chatbot) is in Python’s path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
import faiss
import json
from sentence_transformers import SentenceTransformer



#loading embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384  #no of vectors dimension
index = faiss.IndexFlatL2(dimension)

def load_knowledge_base():
    with open("chatbot/knowledge_base.json", "r") as file:
        return json.load(file)

knowledge_base = load_knowledge_base()

#converts questions into embedding and add into faiss index
faq_keys = list(knowledge_base.keys())
faq_embeddings = embedding_model.encode(faq_keys)
index.add(faq_embeddings)       

#Define greeting & goodbyes
greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
goodbyes = ["bye", "goodbye", "end","okay","ok", "exit", "thanks", "thank you"]

def chatbot_response(query: str, first_message: False): 
    print("Chatbot: 👋 Hello! I'm your IT Support Assistant. How can I assist you today?")
#converts query into lowercase for matching
    query_lower = query.lower()

    #if first_message:
     #   return {"response": "👋 Hello! I'm your IT Support Assistant. How can I assist you today?"}
    #check for greeting messages
    if any(word in query_lower for word in greetings):
        return {"response": "👋 Hey there! How can I help you today?"}
    
     # Check for goodbye messages
    if any(word in query_lower for word in goodbyes):
        return {"response": "👋 Goodbye! Have a great day! 😊"}
    
    if "status" in query_lower or "ticket" in query_lower:
        from chatbot.ticketing import get_ticket
        ticket_id_match = re.search(r'(\bIA-\d+\b)', query)  # Extract ticket ID like IA-123
        if ticket_id_match:
            ticket_id = ticket_id_match.group(1)  # Get ticket ID from query
            status = get_ticket(ticket_id)  # Fetch ticket status
            return {"response": f"Your ticket {ticket_id} is currently: {status}"}
        else:
            return {"response": "Please provide a valid ticket ID (e.g., IA-123) to check the status."}
   
    
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, 1)
    best_distance = distances[0][0]
    best_index = indices[0][0]
    threshold=1.0
    if best_distance < threshold:
        best_answer = knowledge_base.get(faq_keys[best_index])
        return {"response": best_answer}
    else:
        from chatbot.ticketing import create_ticket
        ticket_id = create_ticket(query)
        message = f"🚨 New IT Support Ticket 🚨\nIssue: {query}\nTicket ID: {ticket_id}"
        requests.post ("https://hooks.slack.com/services/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", json= {"text": message})
        return {"response": f"I couldn't find an answer for this. I've created a ticket for you. Your ticket ID is {ticket_id}."}
    """
if __name__ == "__main__":
    print("Chatbot: 👋 Hello! I'm your IT Support Assistant. How can I assist you today?")
    
    first_message = True  # ✅ First message flag

    while True:
        user_input = input("You: ")  # Get input from the user
        
        if user_input.lower() in ["bye", "exit", "end"]:
            print("Chatbot: 👋 Goodbye! Have a great day! 😊")
            break  # Stop the chatbot
        
        response = chatbot_response(user_input, first_message)  # ✅ Pass first_message
        first_message = False  # ✅ After first greeting, set it to False

        print("Chatbot:", response["response"])
    """