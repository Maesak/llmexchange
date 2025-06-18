from langchain.tools import tool
from api.frankfurter_api import convert_currency
from utils.parser import parse_query_openrouter
import ast

@tool
def parser_tool(user_query: str) -> dict:
    """Parse the user query into structured currency conversion intent."""
    return parse_query_openrouter(user_query)

@tool
def convert_tool(parsed_result: str) -> str:
    """Convert currency using structured input: amount, from_currency, to_currency."""
    if '{' in parsed_result:
        parsed_result = ast.literal_eval(parsed_result)  # Convert string representation of dict to actual dict
    else:
        parsed_result = parse_query_openrouter(parsed_result)  # Parse the query if not already a dict
    if not isinstance(parsed_result, dict):
        return "Invalid input format. Please provide a structured query with amount, source currency, and destination currency."
    required_keys = ["amount", "from_currency", "to_currency"]
    if not all(parsed_result.get(k) for k in required_keys):
        return "Missing one or more required fields. Please provide amount, source currency, and destination currency."

    result = convert_currency(
        parsed_result["amount"],
        parsed_result["from_currency"],
        parsed_result["to_currency"]
    )
    return (
        f"{parsed_result['amount']:.2f} {parsed_result['from_currency']} = {result['converted']:.2f} "
        f"{parsed_result['to_currency']} (Rate: {result['rate']}, Date: {result['ts'].date()})"
    )

@tool
def clarify_tool(parsed_result: str) -> str:
    """Ask the user to clarify missing info (amount, from_currency, to_currency)."""
    if '{' in parsed_result:
        parsed_result = ast.literal_eval(parsed_result)  # Convert string representation of dict to actual dict
    else:
        parsed_result = parse_query_openrouter(parsed_result) 

    missing = []
    if not parsed_result.get("amount"): missing.append("amount")
    if not parsed_result.get("from_currency"): missing.append("source currency")
    if not parsed_result.get("to_currency"): missing.append("destination currency")
    return f"To proceed, I need: {', '.join(missing)}. Could you please provide them?"

@tool
def refuse_tool() -> str:
    """Refuse queries unrelated to currency conversion."""
    return "I'm only able to help with currency conversions right now. Please ask me something like 'Convert 50 USD to EUR'."
