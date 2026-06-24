from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_datetime(format: str = "full") -> str:
    """
    Get current date and time.
    format: "date", "time", or "full" (default)
    """
    now = datetime.now()
    if format == "date":
        return now.strftime("%Y-%m-%d")
    elif format == "time":
        return now.strftime("%H:%M:%S")
    else:
        return now.strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate_date_difference(date1: str, date2: str) -> str:
    """
    Calculate days between two dates.
    Input format: YYYY-MM-DD
    """
    try:
        d1 = datetime.strptime(date1.strip(), "%Y-%m-%d")
        d2 = datetime.strptime(date2.strip(), "%Y-%m-%d")
        diff = abs((d2 - d1).days)
        return f"{diff} days between {date1} and {date2}"
    except Exception as e:
        return f"Error: {e}. Use format YYYY-MM-DD"