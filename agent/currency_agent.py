import os
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from agent.memory import memory
from agent.prompt import SYSTEM_PROMPT
from agent.tools import parser_tool, convert_tool, clarify_tool, refuse_tool

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("LLM_MODEL", "llama3-8b-8192"),
    temperature=0
)

tools = [
    Tool.from_function(parser_tool, name="parser_tool", description="Parse user query into structured intent"),
    Tool.from_function(convert_tool, name="convert_tool", description="Convert currency from parsed input"),
    Tool.from_function(clarify_tool, name="clarify_tool", description="Ask user to clarify missing conversion fields"),
    Tool.from_function(refuse_tool, name="refuse_tool", description="Refuse unrelated queries politely")
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent_type="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
)

def route_user_query(user_query: str):
    return agent.invoke({"input": user_query})

if __name__ == "__main__":
    while True:
        q = input("You: ")
        if q.lower() in {"exit", "quit"}: break
        response = route_user_query(q)
        print("Bot:", response)

    # user_query = "Convert 60 USD to INR"
    # response = route_user_query(user_query)
    # print("Generated Response:", response)

