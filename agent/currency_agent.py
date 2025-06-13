# import os
# import requests
# from agent.prompt import SYSTEM_PROMPT
# from utils.read_yaml import read_yaml

# # Load the system prompt from a YAML file
# config = read_yaml("config/model_config.yaml")

# def generate_dynamic_response(user_query: str, parsed_result: dict):
#     prompt = SYSTEM_PROMPT.strip()

#     messages = [
#         {"role": "system", "content": prompt},
#         {"role": "user", "content": f"""
#     User message: {user_query}

#     Parsed result:
#     {parsed_result}
#     """}
#     ]

#     headers = {
#         "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers=headers,
#         json={
#             "model": config["model"],  # e.g., mistral-7b-instruct
#             "messages": messages
#         }
#     )

#     print("\n\n2. Response Status Code:", response.status_code)

#     return response.json()["choices"][0]["message"]["content"]


# if __name__ == "__main__":

#     from utils.parser import parse_query_openrouter

#     user_query = "Convert 50 USD to INR"
#     parsed_result = parse_query_openrouter(user_query)

#     print("Parsed Result:", parsed_result)

#     response = generate_dynamic_response(user_query, parsed_result)
#     print("Generated Response:", response)

# ===================================#

# from langchain.agents import initialize_agent, Tool
# from langchain_groq import ChatGroq
# from agent.prompt import SYSTEM_PROMPT
# from agent.tools import convert_tool, clarify_tool, refuse_tool
# from agent.memory import memory
# import os
# from utils.read_yaml import read_yaml
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load the system prompt from a YAML file
# config = read_yaml("config/model_config.yaml")



# SYSTEM_PROMPT = """
# You are a helpful and polite assistant that only supports currency conversion queries.
# You are having access to 3 tools: convert_tool, clarify_tool, and refuse_tool.
# Based on structured input from a parser, decide which tool to invoke.

# Use the following logic:
# - If all of amount, from_currency, and to_currency are present and valid → use convert_tool
# - If one or more fields are missing but intent is clear → use clarify_tool
# - If user intent is unrelated to currency conversion → use refuse_tool
# - Do NOT pass a string like '100 USD to EUR'. Always pass the parsed structured key-value inputs. 
# e.g 
# {
#   "action": "", 
#   "amount": , 
#   "from_currency": , 
#   "to_currency":  
#   }

# Here are some examples of input and tool decisions:

# ### Example 1
# Parsed Input:
# {
#   "action": "convert",
#   "amount": 100,
#   "from_currency": "USD",
#   "to_currency": "EUR"
# }
# Response:
# Use convert_tool with:
# {
#   "amount": 100,
#   "from_currency": "USD",
#   "to_currency": "EUR"
# }

# ### Example 2
# Parsed Input 2:
# {
#   "action": "clarify",
#   "amount": 100,
#   "from_currency": "USD",
#   "to_currency": null
# }
# Response 2: Use clarify_tool and mention missing destination currency.

# ### Example 3
# Parsed Input 3:
# {
#   "action": "refuse",
#   "amount": null,
#   "from_currency": null,
#   "to_currency": null
# }
# Response 3: Use refuse_tool and respond politely.

# Always pick the correct tool based on input.
# """





# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model=config["LLM"],
#     temperature=0
# )

# tools = [
#     Tool.from_function(
#         func=convert_tool,
#         name="convert_tool",
#         description="Use this to convert currency when amount, source and target currencies are present."
#     ),
#     Tool.from_function(
#         func=clarify_tool,
#         name="clarify_tool",
#         description="Use this when any required currency information is missing in the parsed input."
#     ),
#     Tool.from_function(
#         func=refuse_tool,
#         name="refuse_tool",
#         description="Use this to politely refuse queries unrelated to currency conversion."
#     )
# ]

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     memory=memory,
#     agent_type="chat-zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True,
#     input_variables=["input"]
# )

# def route_parsed_query(parsed_result: dict) -> str:
#     # Only structured data passed — not raw user message
#     return agent.invoke({"input": parsed_result})
#     # return agent.invoke(parsed_result)

# if __name__ == "__main__":
#     from utils.parser import parse_query_openrouter

#     user_query = "Convert 60 USD to INR"
#     parsed_result = parse_query_openrouter(user_query)

#     print("Parsed Result:", parsed_result)

#     print(type(parsed_result))  # Should be a dict
#     print(parsed_result)

#     response = route_parsed_query(parsed_result)
#     print("Generated Response:", response)

# =================================== #

# import os
# from langchain.agents import initialize_agent, Tool
# from langchain_groq import ChatGroq
# from agent.memory import memory
# from agent.prompt import SYSTEM_PROMPT
# from agent.tools import convert_tool, clarify_tool, refuse_tool
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model=os.getenv("LLM_MODEL", "llama3-8b-8192"),
#     temperature=0
# )

# tools = [
#     Tool.from_function(
#         func=convert_tool,
#         name="convert_tool",
#         description="Convert currency when full amount, source, and target are present."
#     ),
#     Tool.from_function(
#         func=clarify_tool,
#         name="clarify_tool",
#         description="Ask clarifying question when part of the conversion info is missing."
#     ),
#     Tool.from_function(
#         func=refuse_tool,
#         name="refuse_tool",
#         description="Refuse politely if the user isn't asking about currency conversion."
#     ),
# ]

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     memory=memory,
#     agent_type="chat-zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True
# )

# def route_user_query(user_query: str):
#     return agent.invoke({"input": user_query})


# if __name__ == "__main__":
#     # while True:
#     #     q = input("You: ")
#     #     if q.lower() in {"exit", "quit"}: break
#     #     response = route_user_query(q)
#     #     print("Bot:", response)

#     user_query = "Convert 60 USD to INR"
# #     parsed_result = parse_query_openrouter(user_query)

# #     print("Parsed Result:", parsed_result)

# #     print(type(parsed_result))  # Should be a dict
# #     print(parsed_result)

#     response = route_user_query(user_query)
#     print("Generated Response:", response)


# =================================== #

import os
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from agent.memory import memory
from agent.prompt import SYSTEM_PROMPT
from agent.tools import parser_tool, convert_tool, clarify_tool, refuse_tool
from agent.output_parser import FinalizingOutputParser

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
    output_parser=FinalizingOutputParser()
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

