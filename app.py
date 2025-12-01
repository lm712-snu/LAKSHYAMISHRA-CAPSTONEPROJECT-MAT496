import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# LangChain & Graph Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional, Any
from datetime import datetime, timedelta
import re

# Load Environment Variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Legal AI Agent", page_icon="⚖️", layout="wide")

st.title("⚖️ Contract QA & Risk Analyzer Agent")
st.markdown("Upload a legal contract (PDF) and ask questions about obligations, risks, and deadlines.")

# --- 1. DEFINE DATA MODELS ---
class ClauseReference(BaseModel):
    id: str = Field(description="Clause ID or Section Number")
    text: str = Field(description="The relevant text snippet")

class LegalResponse(BaseModel):
    summary: str = Field(description="Executive summary of the answer")
    obligations: List[str] = Field(description="List of obligations")
    risks: List[str] = Field(description="List of risks/penalties")
    supporting_clauses: List[ClauseReference] = Field(description="Evidence clauses")

# --- 2. DEFINE TOOLS ---
@tool
def calculate_deadline(start_date_str: str, days: int) -> str:
    """Calculates deadline date given start date (YYYY-MM-DD) and days."""
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        deadline = start_date + timedelta(days=days)
        return deadline.strftime("%Y-%m-%d")
    except ValueError:
        return "Error: Use YYYY-MM-DD format."

@tool
def extract_monetary_values(text: str) -> list:
    """Extracts money values."""
    pattern = r'(\$|USD|€|EUR|£)\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
    return re.findall(pattern, text)

# --- 3. CORE LOGIC (CACHED) ---

@st.cache_resource
def process_pdf(file_path):
    """
    Ingest -> Chunk -> Index
    Cached so we don't re-process the same file repeatedly.
    """
    # 1. Ingest
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text = "\n\n".join([p.page_content for p in pages])
    
    # 2. Chunk
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.create_documents([text])
    
    # 3. Embed & Index
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    return vector_store

def analyze_query(vector_store, query):
    """
    Retrieve -> Analyze (RAG)
    """
    # 1. Retrieve
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    context_str = "\n\n".join([f"[Clause {i+1}]: {d.page_content}" for i, d in enumerate(docs)])
    
    # 2. Analyze with LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = [calculate_deadline, extract_monetary_values]
    structured_llm = llm.bind_tools(tools).with_structured_output(LegalResponse)
    
    system_msg = """You are an expert Legal AI Agent. 
    Answer STRICTLY based on the provided clauses. 
    Identify obligations, risks, and financial terms.
    If dates are relative, use tools to calculate them."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "Context:\n{context}\n\nUser Query: {query}")
    ])
    
    chain = prompt | structured_llm
    response = chain.invoke({"context": context_str, "query": query})
    return response

# --- 4. SIDEBAR: FILE UPLOAD ---
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload PDF Contract", type=["pdf"])
    
    api_key = st.text_input("OpenAI API Key (Optional)", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# --- 5. MAIN APP FLOW ---

if "messages" not in st.session_state:
    st.session_state.messages = []

if not os.environ.get("OPENAI_API_KEY"):
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar or .env file.")
    st.stop()

if uploaded_file:
    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    with st.spinner("Processing Document... (Ingesting, Chunking, Indexing)"):
        try:
            vector_store = process_pdf(temp_path)
            st.success("✅ Document processed! You can now ask questions.")
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.stop()

    # Chat Interface
    query = st.chat_input("Ask about penalties, dates, or obligations...")
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query:
        # User Message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        # AI Processing
        with st.chat_message("assistant"):
            with st.spinner("Analyzing legal clauses..."):
                try:
                    response = analyze_query(vector_store, query)
                    
                    # Format Output nicely
                    output_md = f"### 📝 Summary\n{response.summary}\n\n"
                    
                    if response.obligations:
                        output_md += "### 👮 Obligations\n" + "\n".join([f"- {item}" for item in response.obligations]) + "\n\n"
                        
                    if response.risks:
                        output_md += "### ⚠️ Risks & Penalties\n" + "\n".join([f"- {item}" for item in response.risks]) + "\n\n"
                        
                    # Display Main Response
                    st.markdown(output_md)
                    
                    # Display Evidence in Expander
                    with st.expander("🔍 View Supporting Evidence (Clauses)"):
                        for clause in response.supporting_clauses:
                            st.markdown(f"**{clause.id}**: *{clause.text}*")
                            
                    # Add to history (store markdown representation)
                    st.session_state.messages.append({"role": "assistant", "content": output_md})
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.info("👋 Please upload a PDF document in the sidebar to begin.")