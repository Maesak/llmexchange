# from utils.parser import parse_query_openrouter
from agent.currency_agent import route_user_query

def main():
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]: 
            break

        # parsed = parse_query_openrouter(q)
        result = route_user_query(q)
        print("Bot:", result)
