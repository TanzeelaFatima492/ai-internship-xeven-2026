import time
from agent import agent_executor, tracker

MAX_RETRIES = 3

print("=" * 50)
print("🤖 MULTI-TOOL RESEARCH ASSISTANT")
print("   Tools: Calculator | Web Search | RAG Search | Date/Time")
print("   Memory: ON | Performance Tracking: ON")
print("=" * 50)

while True:
    query = input("\n🧑 You (type 'exit' to quit, 'stats' for report): ")

    if query.lower() == "exit":
        tracker.print_summary()
        tracker.save_log()
        print("Goodbye! 👋")
        break

    if query.lower() == "stats":
        tracker.print_summary()
        continue

    for attempt in range(MAX_RETRIES):
        try:
            response = agent_executor.invoke({"input": query})
            print("\n🤖 Final Answer:")
            print(response["output"])
            break
        except Exception as e:
            print(f"\n❌ Attempt {attempt + 1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                wait = 3
                print(f"Retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                print("Maximum retries reached.")