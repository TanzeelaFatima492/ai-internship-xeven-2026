import os
from dotenv import load_dotenv

# LangChain ke zaroori tools import kar rahe hain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Environment variables ko load karna (.env file se key uthana)
load_dotenv()

# 2. Gemini Model ko initialize karna (Free Tier Model)
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3 # Temperature thoda kam rakha hai taaki AI apni taraf se jhoot na bole
)

# 3. Reusable Prompt Template banana
# Isme do variables hain: {document_content} (file ka data) aur {user_question} (aapka sawal)
qa_prompt = PromptTemplate.from_template(
    "You are a helpful AI Mentor. Read the following document carefully and answer the question "
    "based ONLY on the provided text. If the answer is not in the text, say 'I cannot find the answer.'\n\n"
    "--- DOCUMENT START ---\n"
    "{document_content}\n"
    "--- DOCUMENT END ---\n\n"
    "Question: {user_question}\n"
    "Answer:"
)

# 4. StrOutputParser lagana taaki faltu metadata ke bajaye sirf saaf text response mile
clean_output = StrOutputParser()

# 5. LCEL ka use karke pehli validation chain assemble karna
# Flow: Prompt banega -> Gemini ke paas jayega -> Clean text output aayega
qa_chain = qa_prompt | gemini_model | clean_output

# MAIN EXECUTION CORE (Jahan program chalega)
if __name__ == "__main__":
    file_name = "internship_rules.txt"
    
    # Check karna ke kya hamari text file folder mein mojood hai ya nahi
    if not os.path.exists(file_name):
        print("Error: file not found")
    else:
        print(f"📄 Loading your document: {file_name}...")
        
        # Task 2 wala loader use karke file parhna
        loader = TextLoader(file_name)
        loaded_docs = loader.load()
        
        # File ka saara raw text nikalna
        raw_text = loaded_docs[0].page_content
        
        # --- TASK 3 BONUS: Handling Long Documents (Context Limits) ---
        # Hum characters count kar rahe hain. Standard limit humne 4000 characters rakh di hai.
        # Agar text is se bada hoga toh hum usay cut (truncate) kar denge taaki Gemini crash na ho.
        MAX_CHAR_LIMIT = 4000
        
        if len(raw_text) > MAX_CHAR_LIMIT:
            print(f"⚠️ Warning: File kaafi badi hai ({len(raw_text)} chars). Context window bachaane ke liye isay cut kiya ja raha hai...")
            raw_text = raw_text[:MAX_CHAR_LIMIT] # Text ko limit tak kaat diya
        else:
            print("✅ File size check passed. Loading full content into the prompt.")
            
        print("-" * 50)
        
        # --- AI SE QUESTIONS POOCHNA ---
        # Test Case 1: Summarize karne ka sawal
        question_1 = "Summarize this document in 3 bullet points."
        print(f"\n❓ Question 1: {question_1}")
        
        # Chain ko dono zaroori inputs (file ka data + hamara sawal) de kar chalana
        response_1 = qa_chain.invoke({
            "document_content": raw_text,
            "user_question": question_1
        })
        print(f"🤖 AI Answer:\n{response_1}\n")
        
        print("-" * 50)
        
        # Test Case 2: Key points nikalne ka sawal
        question_2 = "What are the core key points or takeaways from this text?"
        print(f"\n❓ Question 2: {question_2}")
        
        response_2 = qa_chain.invoke({
            "document_content": raw_text,
            "user_question": question_2
        })
        print(f"🤖 AI Answer:\n{response_2}")
        print("-" * 50)