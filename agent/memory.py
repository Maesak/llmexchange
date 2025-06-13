from langchain.memory import ConversationBufferMemory
# from langchain.schema import messages_from_dict, messages_to_dict

# Create an in-memory store
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="user_query",      
    output_key="agent_response", 
    return_messages=True         
)

# Optional: Save/load interface
def get_chat_history():
    return memory.load_memory_variables({})["chat_history"]

def save_to_memory(user_query: str, agent_response: str):
    memory.save_context(
        {"user_query": user_query},
        {"agent_response": agent_response}
    )
def clear_memory():
    memory.clear()
    print("Memory cleared.")

def print_memory():
    chat_history = get_chat_history()
    for message in chat_history:
        print(f"{message['role']}: {message['content']}")