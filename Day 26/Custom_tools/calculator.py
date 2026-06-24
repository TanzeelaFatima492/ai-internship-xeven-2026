from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result.

    Args:
        expression: Mathematical expression such as '23 * 45'

    Returns:
        Result of calculation.
    """
    try:
        allowed_chars = "0123456789+-*/(). "

        if not all(char in allowed_chars for char in expression):
            return "Error: Invalid characters in expression."

        result = eval(expression)

        return f"Result: {result}"

    except ZeroDivisionError:
        return "Error: Division by zero."

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    expression = input("Enter expression: ")
    print(calculator.invoke(expression))