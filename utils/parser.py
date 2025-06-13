import os
import requests
import json
from dotenv import load_dotenv
from agent.prompt import PARSER_PROMPT_TEMPLATE
from utils.read_yaml import read_yaml

# Load environment variables
load_dotenv()

# Load configuration from YAML file
config = read_yaml("config/model_config.yaml")

API_KEY = os.getenv("OPENROUTER_API_KEY") 

def parse_query_openrouter(user_query):
    prompt = PARSER_PROMPT_TEMPLATE + "\n\n" + user_query.strip() + "\n\nNow analyze the below query and return output as the provided schema\n\n"
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": config["PARSER_MODEL"],  
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }

    response = requests.post(url, headers=headers, json=payload)
    # print("Full Response JSON:", response.json()) 

    print("\n\nParser Response Status Code:", response.status_code)
    print("\n\nParser Raw Response:", response.text)
    # print("\n\n")

    content = response.json()["choices"][0]["message"]["content"]
    if response.status_code != 200:
        print("API call failed:", response.status_code, response.text)
        return {"action": "refuse", "amount": None, "from_currency": None, "to_currency": None}

    try:
        content = response.json()
        message = content["choices"][0]["message"]["content"]
        return json.loads(message)
    except Exception as e:
        print("JSON parsing error:", e)
        return {"action": "refuse", "amount": None, "from_currency": None, "to_currency": None}
if __name__ == "__main__":

    ## -------------------- ##  
    # Example usage
    # result = parse_query_openrouter("INR 50")                          # clarify
    result = parse_query_openrouter("Convert 100 USD to EUR")            # convert
    # result = parse_query_openrouter("How much is 20 GBP?")             # clarify
    # result = parse_query_openrouter("What's the weather like today?")  # refuse
    print(result)