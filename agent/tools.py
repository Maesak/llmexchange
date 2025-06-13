from langchain.tools import tool
from api.frankfurter_api import convert_currency

# # @tool
# # def convert_tool(parsed_user_query: dict) -> str:
# #     """Convert amount from one currency to another."""
# #     print("Request received for currency conversion. convert_tool() invoked.")
# #     amount = parsed_user_query["amount"]
# #     from_currency = parsed_user_query["from_currency"]
# #     to_currency = parsed_user_query["to_currency"]
# #     print(f"Converting {amount} from {from_currency} to {to_currency}")
# #     result = convert_currency(amount, from_currency, to_currency)
# #     return (
# #         f"""{amount:.2f} {from_currency.upper()} = {result['converted']:.2f}
# #         {to_currency.upper()} (Rate: {result['rate']}, Date: {result['ts'].date()})"""
# #     )

# from langchain.tools import tool

# @tool
# def convert_tool(amount: float, from_currency: str, to_currency: str) -> str:
#     """Convert amount from one currency to another."""
#     print("Request received for currency conversion. convert_tool() invoked.")
#     print(f"Converting {amount} from {from_currency} to {to_currency}")
#     result = convert_currency(amount, from_currency, to_currency)
#     return (
#         f"""{amount:.2f} {from_currency.upper()} = {result['converted']:.2f}
#         {to_currency.upper()} (Rate: {result['rate']}, Date: {result['ts'].date()})"""
#     )

# @tool
# def clarify_tool(user_query: str, parsed_result: dict) -> str:
#     """Ask the user a clarifying question when the request is incomplete."""
#     missing = []
#     if not parsed_result.get("amount"): missing.append("amount")
#     if not parsed_result.get("from_currency"): missing.append("source currency")
#     if not parsed_result.get("to_currency"): missing.append("destination currency")

#     print("Clarification needed. clarify_tool() invoked.")
#     print(f"Missing information: {', '.join(missing)}")
#     if not missing:
#         return "It seems like you want to convert currency, but I need more information."
    
#     return f"It looks like you want to convert currency, but I need the following info: {', '.join(missing)}."

# @tool
# def refuse_tool(user_query: str) -> str:
#     """Politely refuse unrelated queries."""

#     print("Unrelated query received. refuse_tool() invoked.")

#     return "I'm only able to help with currency conversions at the moment. Please provide an amount and currencies to convert."


# from langchain.tools import tool
# from api.frankfurter_api import convert_currency
# from utils.parser import parse_query_openrouter

# @tool
# def convert_tool(user_query: str) -> str:
#     """Use when the user asks to convert currency with a complete request."""
#     parsed = parse_query_openrouter(user_query)

#     # Validate parsed values
#     if not all([parsed.get("amount"), parsed.get("from_currency"), parsed.get("to_currency")]):
#         return (
#             "I tried to process your request, but some information is still missing. "
#             "Please make sure to include amount, source currency, and destination currency."
#         )

#     result = convert_currency(parsed["amount"], parsed["from_currency"], parsed["to_currency"])
#     return (
#         f"{parsed['amount']:.2f} {parsed['from_currency']} = {result['converted']:.2f} "
#         f"{parsed['to_currency']} (Rate: {result['rate']}, Date: {result['ts'].date()})"
#     )


# @tool
# def clarify_tool(user_query: str) -> str:
#     """Use when the user query is a currency conversion request but lacks some fields."""
#     parsed = parse_query_openrouter(user_query)
#     missing = []
#     if not parsed.get("amount"): missing.append("amount")
#     if not parsed.get("from_currency"): missing.append("source currency")
#     if not parsed.get("to_currency"): missing.append("destination currency")
#     return f"It looks like you're asking for a currency conversion, but I'm missing the following info: {', '.join(missing)}."

# @tool
# def refuse_tool(user_query: str) -> str:
#     """Use when the query is unrelated to currency conversion."""
#     return "I'm only able to help with currency conversions. Please ask me something like 'Convert 50 USD to EUR'."


### agent/tools.py

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
