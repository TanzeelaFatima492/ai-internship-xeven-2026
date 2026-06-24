from langchain_core.tools import tool
import re

@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions like 1970/4, 25*3, 100+50"""
    try:
        # Allow only numbers and basic operators for safety
        cleaned = re.sub(r'[^0-9+\-*/.() ]', '', expression)
        cleaned = cleaned.replace(" ", "")
        if not cleaned:
            return "Error: No valid expression found"
        result = eval(cleaned)
        return str(result)
    except Exception as e:
        return f"Error: {e}"