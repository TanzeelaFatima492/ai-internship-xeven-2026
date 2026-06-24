import time
from agent import agent_executor

MAX_RETRIES = 3

while True:
    query = input("\nAsk Anything (type exit to quit): ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    for attempt in range(MAX_RETRIES):
        try:
            response = agent_executor.invoke({"input": query})
            print("\nFinal Answer:\n")
            print(response["output"])
            break
        except Exception as e:
            print(f"\nAttempt {attempt + 1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                wait = (attempt + 1) * 5
                print(f"Waiting {wait} seconds before retry...")
                time.sleep(wait)
            else:
                print("\nMaximum retries reached. Try again later.")