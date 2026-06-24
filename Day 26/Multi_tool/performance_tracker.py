import json
import time
from datetime import datetime

class PerformanceTracker:
    def __init__(self, log_file="performance_log.json"):
        self.log_file = log_file
        self.tool_calls = {}      # tool_name → count
        self.success_count = {}
        self.total_time = {}      # tool_name → total seconds
        self.session_start = time.time()

    def record_call(self, tool_name: str, success: bool, duration: float):
        self.tool_calls[tool_name] = self.tool_calls.get(tool_name, 0) + 1
        if success:
            self.success_count[tool_name] = self.success_count.get(tool_name, 0) + 1
        self.total_time[tool_name] = self.total_time.get(tool_name, 0) + duration

    def get_stats(self):
        stats = {
            "session_duration_seconds": round(time.time() - self.session_start, 1),
            "tools": {}
        }
        for tool in self.tool_calls:
            calls = self.tool_calls[tool]
            successes = self.success_count.get(tool, 0)
            stats["tools"][tool] = {
                "calls": calls,
                "success_rate": f"{(successes/calls)*100:.1f}%" if calls > 0 else "0%",
                "avg_time_seconds": round(self.total_time.get(tool, 0) / calls, 3) if calls > 0 else 0
            }
        return stats

    def save_log(self):
        with open(self.log_file, "w") as f:
            json.dump(self.get_stats(), f, indent=2)

    def print_summary(self):
        stats = self.get_stats()
        print("\n" + "="*50)
        print("📊 PERFORMANCE REPORT")
        print("="*50)
        print(f"Session: {stats['session_duration_seconds']} seconds")
        for tool, data in stats["tools"].items():
            print(f"\n🔧 {tool}")
            print(f"   Calls: {data['calls']}")
            print(f"   Success Rate: {data['success_rate']}")
            print(f"   Avg Time: {data['avg_time_seconds']}s")
        print("="*50)