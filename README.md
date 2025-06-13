# LLMExchange – LLM-Powered Currency Converter Agent

LLMExchange is an intelligent currency conversion assistant powered by LangChain Agnets & Tools and LLMs.  
It understands natural language queries, maintains conversation history, and uses the Frankfurter API for real-time currency conversion.

#### 🏗 Architecture
1. **LLM Input** → raw user query
2. **parser_tool** → extracts structured data
3. **Routing Decision**:
   - `convert_tool` → complete conversion info
   - `clarify_tool` → partial info, needs clarification
   - `refuse_tool` → irrelevant query
4. **langchain orchestration** → connects agents & tools
5. **ConversationBufferMemory** → saves memory and clarifies inaccurate queries.

#### ⚙️ Tech Stack
- LLM: Mistral (via Groq)
- mistral via OprnRouter
- LangChain (Tools + AgentExecutor)
- Frankfurter API (live exchange rates)
- Python 3.12, dotenv, requests

## Draft Architecture
[Initial draft (WIP)](./screenshots/draft-architecture.png)