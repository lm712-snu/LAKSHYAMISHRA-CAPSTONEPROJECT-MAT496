# Title: **Legal Document Question-Answering & Contract Analyzer Agent (LangGraph)**

## Overview

The **Contract Analyzer & Legal QA Agent** is an automated LangGraph-powered system that reads long and complex legal documents (contracts, policies, agreements), breaks them into semantically meaningful chunks, indexes them, and answers user questions with reliable, evidence-based responses.

The system supports:

* Clause extraction
* Summaries of sections
* Risk & anomaly detection
* Identification of obligations, penalties, deadlines
* Structured output for downstream use
* RAG-based question answering using semantic search
* Tool-calling for date normalization, amount extraction, or clause classification

This project is useful for anyone who wants to quickly understand a legal document without reading 40–200 pages manually.

---

## Reason for picking this project

This project fits perfectly with the course concepts. It uses:

### ✔ Prompting

Specialized prompts for clause extraction, risk detection, legal summaries.

### ✔ Structured Output

All final answers are returned as JSON with mandatory keys: `summary`, `risks`, `answers`, `supporting_clauses`.

### ✔ Semantic Search

All legal document segments are embedded and stored in a vector index for quick clause-level retrieval.

### ✔ RAG (Retrieval-Augmented Generation)

Queries are answered *only* based on retrieved clauses, making the output verifiable.

### ✔ Tool Calling

* A date parser tool (to convert "30 days from signing" → actual date)
* A money extraction tool
* A classification tool for contract clauses (payment, liability, confidentiality, termination, etc.)

### ✔ LangGraph (State, Nodes, Graph)

Nodes: Ingest → Chunk → Embed → Index → Retrieve → Analyze → Format JSON

### ✔ LangSmith

Used to observe node-level traces, debug prompt issues, and inspect final JSON validity.

This project demonstrates creativity by applying LangGraph to a realistic legal automation task.

---

## Video Summary Link

(Add link after you record; YouTube or Drive)

**Your video must include:**

* Your face visible
* 3–5 minute explanation
* Overview of what the agent does
* Inputs + outputs demonstration
* Example run on a sample contract PDF

---

## Plan

For each step below:

* Implement the step
* Change `[TODO]` → `[DONE]`
* Commit with the recommended commit message
* Spread commits across *at least two dates*

---

### **Project Roadmap**

* [TODO] **Step 1 — Repository Setup & Sample Data**

  * Add sample legal documents (PDF/Markdown)
  * Create folders: `graphs/`, `nodes/`, `data/`, `tools/`
  * Commit msg: `chore: initial scaffold and sample documents`

* [TODO] **Step 2 — Ingest & Chunk Node**

  * Extract text from PDF
  * Split into clauses using legal heuristics
  * Commit msg: `feat(ingest): add PDF loader and clause chunker`

* [TODO] **Step 3 — Embeddings & Vector Index**

  * Use OpenAI / local embeddings
  * Create FAISS or SQLite vector store
  * Commit msg: `feat(index): embeddings + FAISS vector index`

* [TODO] **Step 4 — Retrieval Node**

  * Query embedding → nearest clause retrieval
  * Commit msg: `feat(retrieve): semantic clause retrieval`

* [TODO] **Step 5 — Legal Analysis Node (RAG)**

  * Generate structured answers based only on retrieved clauses
  * Provide: obligations, penalties, key parties, deadlines
  * Commit msg: `feat(rag): legal clause analysis RAG node`

* [TODO] **Step 6 — Tool Calling Integration**

  * Add tools: date parser, amount extractor, clause classifier
  * Commit msg: `feat(tools): add legal tools and integrate with graph`

* [TODO] **Step 7 — Output Formatting Node**

  * Validate JSON schema
  * Re-ask model if invalid
  * Commit msg: `feat(format): enforce JSON schema with retry`

* [TODO] **Step 8 — LangSmith Tracing**

  * Add tracing to each node
  * Commit msg: `chore(debug): integrate LangSmith tracing`

* [TODO] **Step 9 — Notebook Demo & Final README**

  * Show example QAs on contract
  * Add final video link
  * Commit msg: `docs: final documentation + demo notebook`

---

## Example Project Structure

```
contract-qa-agent/
├── README.md
├── main.py
├── data/
│   ├── sample_contract.pdf
│   └── vector_index.faiss
├── graphs/
│   └── contract_graph.py
├── nodes/
│   ├── ingest_node.py
│   ├── chunk_node.py
│   ├── embed_node.py
│   ├── retrieve_node.py
│   ├── analyze_node.py
│   └── format_node.py
├── tools/
│   ├── date_parser.py
│   ├── money_extractor.py
│   └── clause_classifier.py
└── notebooks/
    └── demo.ipynb
```

---

## JSON Output Schema

```json
{
  "query": "What are the penalties for late payment?",
  "summary": "Short answer using retrieved clauses.",
  "obligations": ["Payment must be made within 30 days"],
  "penalties": ["1.5% per month interest after due date"],
  "risks": ["Early termination if delay exceeds 90 days"],
  "supporting_clauses": [
    {"id": "clause_12", "text": "Payment is due in 30 days..."}
  ]
}
```

---

## LangGraph Node Architecture

### **1. IngestNode**

Extract text from PDFs, output raw legal content.

### **2. ChunkNode**

Split into clauses based on punctuation, headings, and numbering.

### **3. EmbedNode**

Generate embeddings for semantic search.

### **4. IndexNode**

Store embeddings in FAISS/SQLite.

### **5. RetrieveNode**

Find top-k relevant clauses.

### **6. AnalyzeNode (RAG)**

Run prompting logic:

* obligations
* rights
* penalties
* summarized legal meaning

### **7. FormatOutputNode**

Ensure everything is valid JSON.

---

## Extra Features (for creativity marks)

* Clause similarity search ("find all related clauses")
* Risk scoring model
* Timeline of obligations
* Extract definitions section
* Web UI (Streamlit / React) to upload contracts
* Export structured output as CSV or JSON

---

## Submission Checklist

* [ ] README updated
* [ ] Video link added
* [ ] Commits across 2+ days
* [ ] LangSmith traces available
* [ ] Graph runs end-to-end

---
