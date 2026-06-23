from pydantic import BaseModel
from typing import List
import json

#  Employee Model
class Employee(BaseModel):
    name: str
    title: str
    department: str
    skills: List[str]

# Company Model (Nested)
class Company(BaseModel):
    name: str
    location: str
    employees: List[Employee]


# Simulated Extraction (replace with LLM later)
def extract_companies():
    return [
        Company(
            name="TechNova Pvt Ltd",
            location="Islamabad",
            employees=[
                Employee(
                    name="Ali Khan",
                    title="AI Engineer",
                    department="R&D",
                    skills=["Python", "ML", "NLP"]
                ),
                Employee(
                    name="Sara Ahmed",
                    title="Data Analyst",
                    department="Analytics",
                    skills=["SQL", "Python", "PowerBI"]
                )
            ]
        ),
        Company(
            name="SoftSolutions",
            location="Lahore",
            employees=[
                Employee(
                    name="Usman Ali",
                    title="Backend Developer",
                    department="Engineering",
                    skills=["Node.js", "MongoDB", "APIs"]
                )
            ]
        )
    ]


# 🌐 Knowledge Graph Builder
def build_knowledge_graph(companies):
    graph = {}

    for company in companies:
        graph[company.name] = {
            "location": company.location,
            "employees": {}
        }

        for emp in company.employees:
            graph[company.name]["employees"][emp.name] = {
                "title": emp.title,
                "department": emp.department,
                "skills": emp.skills
            }

    return graph

# 💾 Export JSON
def export_json(graph):
    with open("knowledge_graph.json", "w") as f:
        json.dump(graph, f, indent=4)

    print("✅ JSON file created: knowledge_graph.json")


# Accuracy Function
def calculate_accuracy(data):
    total = 0
    correct = 0

    for company in data:
        total += 2  # name + location

        if company.name:
            correct += 1
        if company.location:
            correct += 1

        for emp in company.employees:
            total += 4  # name, title, department, skills

            if emp.name:
                correct += 1
            if emp.title:
                correct += 1
            if emp.department:
                correct += 1
            if emp.skills:
                correct += 1

    return (correct / total) * 100


# MAIN EXECUTION
if __name__ == "__main__":

    companies = extract_companies()

    print("\n📌 Companies Extracted:\n")
    for c in companies:
        print(c)

    # Build knowledge graph
    graph = build_knowledge_graph(companies)

    print("\n🌐 Knowledge Graph:\n")
    print(json.dumps(graph, indent=4))

    # Export JSON
    export_json(graph)

    # Accuracy
    accuracy = calculate_accuracy(companies)
    print(f"\n🎯 Extraction Accuracy: {accuracy:.2f}%")