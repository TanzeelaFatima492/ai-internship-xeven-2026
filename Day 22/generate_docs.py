import os
import random

os.makedirs("documents", exist_ok=True)

topics = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Python Programming",
    "FAISS Vector Database",
    "LangChain Framework",
    "Natural Language Processing",
    "Data Science",
    "Computer Vision",
    "Big Data",
    "Cyber Security",
    "Cloud Computing",
    "Software Engineering",
    "Operating Systems",
    "Databases"
]

sections = [
    "Introduction",
    "Core Concepts",
    "Applications",
    "Advantages",
    "Limitations",
    "Future Scope"
]

content_pool = [
    "is a very important field in modern technology.",
    "helps in solving real world problems using data.",
    "is widely used in industry applications.",
    "has become essential for AI systems.",
    "improves performance and scalability.",
    "is used in search and recommendation systems."
]

# generate 50 documents
for i in range(1, 51):
    topic = random.choice(topics)
    section = random.choice(sections)

    content = f"{topic} - {section}\n\n"
    for _ in range(8):  # 8 sentences per document
        content += f"{topic} {random.choice(content_pool)}\n"

    file_path = f"documents/doc_{i}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ 50 documents generated successfully inside /documents")