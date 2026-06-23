import json
import os

prompt_templates = {

    "json_output": {
        "system": "You are a strict JSON generator. You must always return valid JSON only. No explanations.",
        "user": """
Convert the input into JSON format.

Rules:
- Follow this schema exactly:
{schema}

- Do not add extra keys
- Do not write explanations
- Ensure valid JSON

Input:
{text}

Constraints:
{constraints}
"""
    },

    "markdown_table": {
        "system": "You are a data formatting assistant that outputs clean Markdown tables.",
        "user": """
Convert the input into a Markdown table.

Rules:
- Use proper column alignment
- Ensure consistent row structure
- Handle missing values as "N/A"

Format:
{format}

Input:
{text}

Constraints:
{constraints}
"""
    },

    "code_generation": {
        "system": "You are a senior software engineer generating clean, production-ready code.",
        "user": """
Generate code based on the requirements.

Language: {language}

Rules:
- Use proper naming conventions
- Add docstrings and comments
- Follow best practices
- Keep code clean and readable

Requirements:
{text}

Constraints:
{constraints}
"""
    }
}

# TEST DATA 
test_cases = [

    # JSON edge case (missing fields)
    {
        "task": "json_output",
        "text": "Name: Ali, Age: 22",
        "schema": '{"name": "string", "age": "integer", "city": "string"}',
        "constraints": "Return complete JSON even if data missing"
    },

    # malformed input
    {
        "task": "json_output",
        "text": "random text without structure !!!",
        "schema": '{"text": "string", "sentiment": "string"}',
        "constraints": "Infer missing values"
    },

    # markdown table normal
    {
        "task": "markdown_table",
        "text": "Apple 1$, Banana 2$, Mango 3$",
        "format": "Fruit | Price",
        "constraints": "2 columns only"
    },

    # markdown table messy input
    {
        "task": "markdown_table",
        "text": "Ali 20 Lahore, Sara, 25",
        "format": "Name | Age | City",
        "constraints": "Fill missing values with N/A"
    },

    # code generation python
    {
        "task": "code_generation",
        "text": "Create a function that calculates factorial",
        "language": "Python",
        "constraints": "Include recursion + docstring"
    },

    # stress test code generation
    {
        "task": "code_generation",
        "text": "Build login system with validation, hashing, error handling",
        "language": "Python",
        "constraints": "Keep secure and modular"
    }
]

#  PROMPT BUILDER
def build_prompt(task, data):
    template = prompt_templates[task]

    if task == "json_output":
        return template["system"], template["user"].format(
            schema=data["schema"],
            text=data["text"],
            constraints=data["constraints"]
        )

    elif task == "markdown_table":
        return template["system"], template["user"].format(
            format=data["format"],
            text=data["text"],
            constraints=data["constraints"]
        )

    elif task == "code_generation":
        return template["system"], template["user"].format(
            language=data["language"],
            text=data["text"],
            constraints=data["constraints"]
        )


#  RUN TESTS
print("\n🚀 ADVANCED OUTPUT CONTROL TESTS\n")

for case in test_cases:
    system, user = build_prompt(case["task"], case)

    print("\n==============================")
    print("TASK:", case["task"])
    print("\n--- SYSTEM ---")
    print(system)
    print("\n--- USER PROMPT ---")
    print(user)

# SAVE TO DAY 19 FOLDER

output_file = {
    "json_output": prompt_templates["json_output"],
    "markdown_table": prompt_templates["markdown_table"],
    "code_generation": prompt_templates["code_generation"]
}

with open("Day 19/advanced_prompt_templates.json", "w") as f:
    json.dump(output_file, f, indent=4)

print("\n✅ Saved in: Day 19/advanced_prompt_templates.json")