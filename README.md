## Title: Legal Document Question-Answering & Contract Analyzer Agent
## Overview:
The Contract Analyzer & Legal QA Agent is a LangGraph-powered application designed to automate the review of complex legal documents. 
Instead of manually reading 50+ page PDF contracts, users can upload a document and ask natural language questions.
The agent ingests the PDF, chunks the text into legal clauses, indexes them using semantic search, and uses a Retrieval-Augmented Generation (RAG) workflow to provide evidence-backed answers. 
It specifically highlights obligations, risks, and penalties, and includes specialized tools to calculate deadlines and extract financial liabilities.


The agent ingests the PDF, chunks the text into legal clauses, indexes them using semantic search, and uses a Retrieval-Augmented Generation (RAG) workflow to provide evidence-backed answers. It specifically highlights obligations, risks, and penalties, and includes specialized tools to calculate deadlines and extract financial liabilities.
Reason for picking this project
This project was chosen because it perfectly synthesizes all the advanced topics covered in the MAT496 course. It transforms a labor-intensive real-world problem (legal review) into an automated pipeline using the following course concepts:
LangGraph (State, Nodes, Graph): The core architecture uses a StateGraph to manage the flow of data (PDF text 
→
→
 Chunks 
→
→
 Vector Store 
→
→
 Retrieval 
→
→
 Analysis).
RAG (Retrieval Augmented Generation): The system answers queries strictly based on the retrieved clauses from the uploaded PDF, ensuring factual accuracy and reducing hallucinations.
Structured Output: The LLM does not just return text; it returns a Pydantic object (LegalResponse) containing specific lists for summary, obligations, risks, and supporting_clauses.
Semantic Search: We use OpenAI Embeddings and FAISS to perform semantic similarity searches to find relevant legal clauses, not just keyword matches.
Tool Calling: The agent is equipped with custom Python tools (e.g., calculate_deadline) which the LLM invokes to resolve relative dates (e.g., "30 days from signing").
Prompting: Specialized system prompts are used to instruct the agent to act as a "Risk-Averse Legal Analyst."
LangSmith: The entire graph execution is traced in LangSmith to debug retrieval quality and LLM reasoning steps.
