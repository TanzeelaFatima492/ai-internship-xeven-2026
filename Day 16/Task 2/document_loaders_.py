import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader,
    CSVLoader
)

# ==========================================
# 1. COMPREHENSIVE EXPERIMENTS FOR INDIVIDUAL LOADERS
# ==========================================

def practice_individual_loaders():
    print("--- 📝 1. TEXT LOADER PRACTICE ---")
    if os.path.exists("sample.txt"):
        txt_loader = TextLoader("sample.txt")
        txt_docs = txt_loader.load()
        # Examining uniform Document structure
        print(f"Type: {type(txt_docs[0])}")
        print(f"Content: {txt_docs[0].page_content}")
        print(f"Metadata: {txt_docs[0].metadata}\n")

    print("--- 🌐 2. WEB BASE LOADER PRACTICE (HTML Extraction) ---")
    try:
        # Scraping a sample structured web page
        web_loader = WebBaseLoader("https://example.com")
        web_docs = web_loader.load()
        print(f"Web Title/Source Metadata: {web_docs[0].metadata}")
        print(f"Clean extracted content snippet: {web_docs[0].page_content[:150].strip()}...\n")
    except Exception as e:
        print(f"Web loader failed or network issue: {e}\n")

    print("--- 📊 3. CSV LOADER PRACTICE (Structured Data) ---")
    if os.path.exists("data.csv"):
        csv_loader = CSVLoader("data.csv")
        csv_docs = csv_loader.load()
        print(f"Total rows converted to documents: {len(csv_docs)}")
        print(f"First Row Document Content:\n{csv_docs[0].page_content}")
        print(f"First Row Metadata: {csv_docs[0].metadata}\n")


# ==========================================
# 2. BUILDING THE GENERIC SMART LOADER FUNCTION
# ==========================================
def smart_generic_loader(file_path_or_url: str):
    """
    Detects file extension or URL patterns dynamically 
    and applies the correct LangChain Document Loader wrapper.
    """
    # Checking if the input is a website URL
    if file_path_or_url.startswith(("http://", "https://")):
        print(f"🌐 URL Detected. Booting WebBaseLoader...")
        return WebBaseLoader(file_path_or_url).load()
        
    # Extracting file extension for local files
    _, extension = os.path.splitext(file_path_or_url.lower())
    
    if extension == ".txt":
        print(f"📄 Text File Detected. Booting TextLoader...")
        return TextLoader(file_path_or_url).load()
        
    elif extension == ".pdf":
        print(f"📕 PDF Document Detected. Booting PyPDFLoader...")
        # PyPDFLoader handles multi-page indexing automatically splits pages into separate elements
        return PyPDFLoader(file_path_or_url).load()
        
    elif extension == ".csv":
        print(f"📊 CSV Spreadsheet Detected. Booting CSVLoader...")
        return CSVLoader(file_path_or_url).load()
        
    else:
        raise ValueError(f"❌ Unsupported format allocation: '{extension}'")


# ==========================================
# 3. RUNNING VERIFICATION TARGETS
# ==========================================
if __name__ == "__main__":
    # Run standalone tests
    practice_individual_loaders()
    
    print("="*60)
    print("🚀 TESTING SMART GENERIC LOADER ENGINE")
    print("="*60)
    
    # Test Generic function with Text file
    if os.path.exists("sample.txt"):
        docs = smart_generic_loader("sample.txt")
        print(f"Successfully loaded {len(docs)} document node(s).\n")
        
    # Test Generic function with Web URL
    docs_web = smart_generic_loader("https://example.com")
    print(f"Successfully loaded {len(docs_web)} document node(s).\n")
    
    # Note on Multi-page PDF execution layout:
    print("💡 PyPDFLoader Context Note:")
    print("When a multi-page PDF is loaded, 'len(docs)' will equal the total number of pages.")
    print("Each page becomes an individual Document object where metadata contains {'page': page_number}.")