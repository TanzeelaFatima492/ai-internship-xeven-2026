# ✦ LangChain Framework Architecture & Core Components

## 1. Introduction & API Abstraction
* **The Paradigm Shift:** Transitioned from raw API orchestration to framework-driven design. LLMs act as stateless engines; LangChain provides the scaffolding to build stateful applications.
* **Unified Abstraction Layer:** Learned how LangChain abstracts multi-vendor API complexity. Switching the underlying model layer from OpenAI to native Google Gemini (`ChatGoogleGenAI`) requires zero structural rewrites of the core application logic.

## 2. Dynamic Component Chains (LCEL)
* **LangChain Expression Language (LCEL):** Mastered the declarative syntax to compose modular pipelines using the bitwise OR (`|`) pipe operator.
* **Data Stream Pipeline:** Engineered an end-to-end operational flow: 
    $$\text{PromptTemplate} \longrightarrow \text{ChatModel} \longrightarrow \text{StrOutputParser}$$
* **Runnable Interface:** Explored the underlying execution protocol that grants every modular block native support for `.invoke()`, `.stream()`, and asynchronous parsing.

## 3. Data Ingestion & Context Engineering
* **Document Loaders:** Implemented `TextLoader`, `PyPDFLoader`, and `CSVLoader` to extract unstructured data into a uniform standard `Document` schema object containing strict `page_content` and geographical `metadata`.
* **Boundary Control:** Developed a runtime defensive check layer to analyze context payload size (character-count arrays) to truncate strings before crossing target model window constraints.