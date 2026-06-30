import os
from dotenv import load_dotenv

# LangChain Google GenAI Integration
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Environment variables load karna
load_dotenv()


# 1. SETUP GOOGLE GEMINI MODEL WRAPPER
# Hum direct Google GenAI ka wrapper use kar rahe hain (100% Free Tier)
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# 2. CREATE REUSABLE PROMPT TEMPLATE
prompt_template = PromptTemplate.from_template(
    "You are an expert AI Engineer. Explain the programming concept of '{concept}' "
    "specifically for a junior intern at {company_name}. Keep it under 3 sentences with a practical example."
)


# 3. BUILD THE FIRST CHAIN USING LCEL
# The '|' operator chains: Prompt -> Gemini -> Output Parser
output_parser = StrOutputParser()
chain = prompt_template | model | output_parser

# 4. EXECUTE & TEST THE CHAIN
if __name__ == "__main__":
    print("🚀 Initializing Native Gemini LCEL Chain Pipeline...\n" + "-"*50)
    
    try:
        input_data = {
            "concept": "Mutable vs Immutable Objects in Python",
            "company_name": "Xeven Solutions"
        }
        
        # Chain execute ho rahi hai
        response = chain.invoke(input_data)
        
        print(f"💡 Input Concept: {input_data['concept']}")
        print(f"🏢 Context: Specialized for {input_data['company_name']}\n")
        print(f"🤖 Gemini AI Mentor Response:\n{response}")
        print("-"*50)
        
    except Exception as e:
        print(f"❌ Execution Failure: {str(e)}")