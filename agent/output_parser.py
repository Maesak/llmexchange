from langchain.agents import AgentOutputParser
from langchain.schema import AgentFinish, AgentAction
import re

class FinalizingOutputParser(AgentOutputParser):
    def parse(self, text: str):
        if text.strip().startswith("FINAL:"):
            return AgentFinish(
                return_values={"output": text.strip()[7:].strip()},
                log=text
            )
        # Fall back to default parser (basic action parsing)
        match = re.search(r"Action: (\\w+)\\nAction Input: (.+)", text, re.DOTALL)
        if match:
            return AgentAction(tool=match[1], tool_input=eval(match[2]), log=text)
        raise ValueError(f"Could not parse LLM output: {text}")
