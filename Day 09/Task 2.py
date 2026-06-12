# Website Visitor Tracker

visitors = (
    ("123.234.234.1", "2026-06-01 10:00:00"),
    ("123.234.234.9", "2026-06-01 10:05:00"),
    ("123.234.234.3", "2026-06-01 10:10:00"),
    ("123.234.234.4", "2026-06-01 10:15:00"),
    ("123.234.234.2", "2026-06-01 10:20:00"),
    ("123.234.234.5", "2026-06-01 10:25:00"),
    ("123.234.234.5", "2026-06-01 10:30:00"),
    ("123.234.234.9", "2026-06-01 10:35:00"),
    ("123.234.234.8", "2026-06-01 10:40:00"),
    ("123.234.234.9", "2026-06-01 10:45:00")
)

# Display all visitors
print("Website Visitors:")
for ip, time in visitors:
    print(ip, "-", time)

# Find repeated visitors
print("\nRepeated Visitors:")
seen = set()

for ip, time in visitors:
    if ip in seen:
        print(ip)
    else:
        seen.add(ip)

# Find unique visitors
unique_visitors = set()

for ip, time in visitors:
    unique_visitors.add(ip)

print("\nUnique Visitors:")
print(unique_visitors)

print("Total Unique Visitors:", len(unique_visitors))