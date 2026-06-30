"""
Week 3 Comprehensive Demo – Streamlit
✅ PDF/TXT upload
✅ Smart chunking (RecursiveCharacterTextSplitter)
✅ FAISS vector store with HuggingFace embeddings
✅ Semantic search (relevance scores)
✅ Structured extraction (Pydantic + local NER model)
✅ Downloadable report
✅ Clear error/warning messages, large file limit
"""

import os
import tempfile
import re
from typing import List
import streamlit as st
from pydantic import BaseModel, Field

# LangChain imports (all stable, no deprecation)
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Local NER (no API needed)
from transformers import pipeline

#   --------------
# Pydantic Entity Schema
#   --------------
class Entities(BaseModel):
    persons: List[str] = Field(default_factory=list, description="People names")
    organizations: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    dates: List[str] = Field(default_factory=list)
    key_terms: List[str] = Field(default_factory=list)

#   --------------
# Page Config
#   --------------
st.set_page_config(page_title="Document Analyzer", layout="wide")
st.title("📄 Comprehensive Document Analyzer")
st.markdown("*Upload, chunk, embed, search, extract entities, and generate a report.*")

#   --------------
# Cached Models (load once, ~500MB download on first run)
#   --------------
@st.cache_resource(show_spinner="Loading models (first time may download ~500MB)...")
def load_models():
    emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    return emb, ner

embeddings, ner_pipeline = load_models()

#   --------------
# Session State (persist across interactions)
#   --------------
for key, default in [
    ("docs_text", ""),
    ("chunks", []),
    ("vectorstore", None),
    ("uploaded_file_name", ""),
    ("extracted_entities", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

#   --------------
# 1. Upload Section
#   --------------
st.header("1. 📤 Upload Document")
uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    # Only process if a new file is uploaded
    if uploaded_file.name != st.session_state.uploaded_file_name:
        with st.spinner("Processing document... (may take a few seconds)"):
            try:
                # Save to temp
                suffix = ".pdf" if uploaded_file.name.lower().endswith(".pdf") else ".txt"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                # Load text
                loader = PyPDFLoader(tmp_path) if suffix == ".pdf" else TextLoader(tmp_path)
                docs = loader.load()
                full_text = " ".join([d.page_content for d in docs]).strip()

                # 🚨 Check if text is empty (scanned PDF, etc.)
                if not full_text:
                    st.error("❌ Could not extract any text from the document. It may be a scanned image or empty.")
                    st.stop()

                total_chars = len(full_text)
                # Warn if large, and truncate for demo (optional)
                if total_chars > 100_000:
                    st.warning(f"⚠️ Document is large ({total_chars} chars). Only first 100,000 characters will be processed.")
                    full_text = full_text[:100_000]

                # Smart Chunking
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    separators=["\n\n", "\n", ".", "?", "!", " ", ""]
                )
                chunks = splitter.split_text(full_text)

                # Create Vector Store
                vectorstore = FAISS.from_texts(chunks, embeddings)

                # Save state
                st.session_state.docs_text = full_text
                st.session_state.chunks = chunks
                st.session_state.vectorstore = vectorstore
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.extracted_entities = None  # reset

                # Cleanup
                os.unlink(tmp_path)

                st.success(f"✅ Document loaded! **{len(chunks)} chunks**, {len(full_text)} characters")

            except Exception as e:
                st.error(f"❌ Processing error: {str(e)}")
                st.stop()
    else:
        st.info("ℹ️ File already loaded. You can now search or extract entities.")

    # Show chunking stats
    if st.session_state.chunks:
        with st.expander("🔍 Chunking Details"):
            st.write(f"Total chunks: {len(st.session_state.chunks)}")
            st.text("First chunk preview (500 chars):")
            st.code(st.session_state.chunks[0][:500], language=None)

    #   --------------
    # 2. Semantic Search
    #   --------------
    st.header("2. 🔎 Semantic Search")
    query = st.text_input("Search query", placeholder="e.g., functional requirements")
    k = st.slider("Results to show", 1, 10, 3)

    if query:
        if st.session_state.vectorstore is None:
            st.warning("⚠️ No document uploaded yet.")
        else:
            try:
                results = st.session_state.vectorstore.similarity_search_with_score(query, k=k)
                st.subheader("Top Matching Chunks")
                for i, (doc, score) in enumerate(results):
                    # Convert L2 distance to a relevance-like score (0-1)
                    relevance = round(1 / (1 + score), 4)
                    with st.container():
                        st.markdown(f"**Result {i+1}** — Relevance: `{relevance}`")
                        st.text(doc.page_content[:600])
                        if len(doc.page_content) > 600:
                            st.caption("... (truncated)")
                        st.divider()
            except Exception as e:
                st.error(f"Search failed: {str(e)}")

    #   --------------
    # 3. Entity Extraction
    #   --------------
    st.header("3. 🧾 Extract Entities")
    if st.button("Extract Entities", help="Run NER model on first 2000 characters"):
        if not st.session_state.docs_text:
            st.warning("Please upload a document first.")
        else:
            with st.spinner("Extracting entities... (first run may download NER model)"):
                try:
                    text_to_ner = st.session_state.docs_text[:2000]  # limit for speed
                    raw_ents = ner_pipeline(text_to_ner)

                    persons, orgs, locs = [], [], []
                    for ent in raw_ents:
                        label = ent["entity_group"]
                        word = ent["word"].strip()
                        if label == "PER":
                            persons.append(word)
                        elif label == "ORG":
                            orgs.append(word)
                        elif label == "LOC":
                            locs.append(word)

                    # Simple date extraction via regex
                    date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2},?\s\d{4}\b'
                    dates = re.findall(date_pattern, text_to_ner, re.IGNORECASE)[:5]

                    # MISC entities as key terms
                    key_terms = list(set(ent["word"] for ent in raw_ents if ent["entity_group"] == "MISC"))[:10]

                    entities_obj = Entities(
                        persons=list(set(persons)),
                        organizations=list(set(orgs)),
                        locations=list(set(locs)),
                        dates=dates,
                        key_terms=key_terms
                    )
                    st.session_state.extracted_entities = entities_obj.model_dump()
                    st.json(st.session_state.extracted_entities)

                except Exception as e:
                    st.error(f"Extraction error: {str(e)}")

    #   --------------
    # 4. Final Report
    #   --------------
    st.header("4. 📊 Final Report")
    if st.button("Generate Report"):
        if not st.session_state.docs_text:
            st.warning("No document to report on.")
        else:
            with st.spinner("Generating report..."):
                report = []
                report.append("=== DOCUMENT ANALYSIS REPORT ===\n")
                report.append(f"File: {st.session_state.uploaded_file_name}")
                report.append(f"Characters: {len(st.session_state.docs_text)}")
                report.append(f"Chunks: {len(st.session_state.chunks)}\n")

                # Add search results (if query exists)
                if query:
                    report.append("--- Semantic Search ---")
                    report.append(f"Query: {query}")
                    # Re-fetch results for report (or use cached)
                    try:
                        results = st.session_state.vectorstore.similarity_search_with_score(query, k=k)
                        for i, (doc, score) in enumerate(results):
                            rel = round(1/(1+score), 4)
                            report.append(f"{i+1}. Relevance: {rel} | {doc.page_content[:200]}...")
                    except:
                        report.append("(Could not retrieve search results)")
                    report.append("")

                # Add entities
                if st.session_state.extracted_entities:
                    e = st.session_state.extracted_entities
                    report.append("--- Extracted Entities ---")
                    report.append(f"Persons: {', '.join(e['persons']) if e['persons'] else 'None'}")
                    report.append(f"Organizations: {', '.join(e['organizations']) if e['organizations'] else 'None'}")
                    report.append(f"Locations: {', '.join(e['locations']) if e['locations'] else 'None'}")
                    report.append(f"Dates: {', '.join(e['dates']) if e['dates'] else 'None'}")
                    report.append(f"Key Terms: {', '.join(e['key_terms']) if e['key_terms'] else 'None'}")
                else:
                    report.append("No entities extracted yet. Use 'Extract Entities' button first.")

                full_report = "\n".join(report)
                st.download_button(
                    label="⬇️ Download Report",
                    data=full_report,
                    file_name="document_report.txt",
                    mime="text/plain"
                )
                st.text_area("Report Preview", full_report, height=300)

else:
    st.info("👆 Upload a PDF or TXT file to get started.")