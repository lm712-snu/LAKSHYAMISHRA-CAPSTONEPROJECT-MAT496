# Contract QA & Risk Analyzer Agent

A Streamlit prototype for asking questions about uploaded PDF contracts using retrieval-augmented generation (RAG), structured responses, and small helper tools.

> **Status:** Academic prototype / in progress. This repository contains a working application path, but the broader LangGraph roadmap documented in earlier project notes is not fully implemented. It is not a substitute for review by a qualified legal professional.

## What the current app does

1. Accepts a PDF contract upload through a Streamlit interface.
2. Extracts PDF text using `PyPDFLoader`.
3. Splits the text into overlapping chunks.
4. Creates embeddings and a FAISS vector index.
5. Retrieves relevant chunks for a user question.
6. Uses an OpenAI chat model to return a structured response with a summary, obligations, risks, and supporting clause snippets.
7. Provides helper tools for calculating a deadline from a date and number of days, and extracting monetary-value patterns.

## Architecture

```text
PDF upload
   ↓
PDF text extraction
   ↓
Chunking (1000 characters, 150 overlap)
   ↓
OpenAI embeddings → FAISS vector index
   ↓
Question → retrieve relevant chunks
   ↓
OpenAI chat model + structured response schema
   ↓
Summary · Obligations · Risks · Supporting clauses
```

## Technology

- **Interface:** Streamlit
- **PDF ingestion:** LangChain community PDF loader
- **Chunking:** RecursiveCharacterTextSplitter
- **Embeddings / language model:** OpenAI integrations
- **Vector retrieval:** FAISS
- **Output validation:** Pydantic structured response model
- **Helper tools:** Python date arithmetic and monetary-pattern extraction

## Run locally

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies used by the application: `streamlit`, `python-dotenv`, `langchain-community`, `langchain-text-splitters`, `langchain-openai`, `langchain-core`, `faiss-cpu`, and `pypdf`.
4. Run `streamlit run app.py`.
5. Provide an OpenAI API key in the app's password field or through a local environment configuration.

Never commit a real API key or other secrets. Keep credentials in a local `.env` file that is excluded from version control.

## Important limitations

- The answer quality depends on the uploaded document, retrieval quality, model behavior, and prompt.
- Retrieved snippets are used as context, but the system does not guarantee legal completeness, correctness, or enforceability.
- The monetary extractor currently uses a narrow regular expression and is not a complete financial parser.
- The current app code is a Streamlit + LangChain pipeline; the repository's planned multi-node LangGraph roadmap should be treated as future work unless implemented in code.
- Do not upload confidential contracts or personal information to an external model unless you have authorization and understand the relevant privacy requirements.

## Academic context

Developed as a MAT496 capstone exploring prompting, structured output, semantic search, RAG, tool calling, and LLM application design.

## Repository contents

- `app.py` — Streamlit application.
- `project.ipynb` — project notebook.
- `README.md` — project overview and setup.

