import json
prompt_library = {
    
    "summarization": {
        "system": "You are an expert summarizer. You convert long text into clear and concise summaries.",
        "user": """
Summarize the following text.

Text: {text}

Constraints: {constraints}

Output Format: {format}
""",
        "examples": [
            {
                "input": "AI is transforming the world by automating tasks and improving decision-making.",
                "output": "AI is transforming industries by automating tasks and enhancing decisions."
            }
        ]
    },

    "extraction": {
        "system": "You are a data extraction assistant. Extract only required information accurately.",
        "user": """
Extract the required information from the text.

Text: {text}

Fields to extract: {format}

Constraints: {constraints}
""",
        "examples": [
            {
                "input": "Name: Ali, Age: 22, City: Lahore",
                "output": {"Name": "Ali", "Age": 22, "City": "Lahore"}
            }
        ]
    },

    "generation": {
        "system": "You are a creative content generator.",
        "user": """
Generate content based on the given input.

Topic: {text}

Constraints: {constraints}

Output Format: {format}
""",
        "examples": [
            {
                "input": "Healthy lifestyle tips",
                "output": "Eat balanced diet, exercise daily, sleep well."
            }
        ]
    },

    "analysis": {
        "system": "You are a data analysis expert. Provide structured insights.",
        "user": """
Analyze the given text and provide insights.

Text: {text}

Analysis Type: {format}

Constraints: {constraints}
""",
        "examples": [
            {
                "input": "Sales increased by 20% in 2025 due to marketing.",
                "output": "Positive growth trend driven by marketing efforts."
            }
        ]
    }
}

# 🧪 FUNCTION TO BUILD PROMPT
def build_prompt(task, text, format_type="plain text", constraints="None"):
    template = prompt_library[task]
    
    system_msg = template["system"]
    
    user_msg = template["user"].format(
        text=text,
        format=format_type,
        constraints=constraints,
        examples=template["examples"]
    )
    
    return {
        "system": system_msg,
        "user": user_msg
    }

# 🚀 TESTING TEMPLATES
test_inputs = [
    {
        "task": "summarization",
        "text": "Artificial Intelligence is a field of computer science that focuses on building smart machines.",
        "format": "1-2 sentence summary",
        "constraints": "Keep it simple"
    },
    {
        "task": "extraction",
        "text": "Name: Sara, Age: 25, Country: Pakistan",
        "format": "Name, Age, Country",
        "constraints": "Return JSON only"
    },
    {
        "task": "generation",
        "text": "Daily productivity tips",
        "format": "Bullet points",
        "constraints": "5 points only"
    },
    {
        "task": "analysis",
        "text": "Revenue increased by 30% due to new product launch.",
        "format": "Business insight",
        "constraints": "Short analysis"
    }
]

# 🧪 RUN TESTS
print("\n🔷 PROMPT TEMPLATE TEST RESULTS\n")

for test in test_inputs:
    result = build_prompt(
        test["task"],
        test["text"],
        test["format"],
        test["constraints"]
    )
    
    print("\n==============================")
    print("TASK:", test["task"])
    print("\n--- SYSTEM MESSAGE ---")
    print(result["system"])
    print("\n--- USER PROMPT ---")
    print(result["user"])

with open("Day 19/prompt_library.json", "w") as f:
    json.dump(prompt_library, f, indent=4)

print("\n Prompt library saved in Day 19 folder")