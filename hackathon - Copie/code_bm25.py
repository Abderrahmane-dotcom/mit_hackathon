#!/usr/bin/env python3
"""
langgraph_bm25.py

- Loads PDFs from ./files
- Splits into chunks, stores metadata (source & chunk_id)
- Builds a BM25 index over the chunks (rank_bm25)
- Provides BM25Retriever.get_relevant_documents(query, k)
- Uses LangGraph StateGraph with 3 agents that call ChatGroq
- Interactive CLI: enter a topic -> run agents pipeline -> print result
"""

import os
import re
from glob import glob
from typing import List, Dict, Any, TypedDict, Optional
from dataclasses import dataclass

# Document loading & splitting
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# LLM
from langchain_groq import ChatGroq

# LangGraph
from langgraph.graph import StateGraph

# BM25
from rank_bm25 import BM25Okapi

# ---------------------------
# Configuration
# ---------------------------
FILES_DIR = "files"  # folder containing PDFs
import os
os.environ["GROQ_API_KEY"] = "put_it_there"

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# ---------------------------
# Simple tokenizer for BM25
# ---------------------------
def simple_tokenize(text: str) -> List[str]:
    tokens = re.findall(r"\w+", text.lower())
    return [t for t in tokens if len(t) > 1]

# ---------------------------
# Data classes
# ---------------------------
@dataclass
class DocChunk:
    page_content: str
    metadata: Dict[str, Any]

# ---------------------------
# Ingestion: load PDFs + chunk
# ---------------------------
def load_and_chunk_pdfs(files_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[DocChunk]:
    chunks: List[DocChunk] = []
    pdf_paths = sorted(glob(os.path.join(files_dir, "*.pdf")))
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for pdf_path in pdf_paths:
        filename = os.path.basename(pdf_path)
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
        except Exception as e:
            print(f"Warning: failed to load {pdf_path}: {e}")
            continue

        for i, d in enumerate(docs):
            if not d.metadata:
                d.metadata = {}
            d.metadata["source"] = filename
            d.metadata["orig_page_index"] = d.metadata.get("page", i)

        doc_chunks = splitter.split_documents(docs)
        for idx, c in enumerate(doc_chunks):
            meta = dict(c.metadata)
            meta["chunk_id"] = f"{filename}__chunk{idx}"
            chunks.append(DocChunk(page_content=c.page_content, metadata=meta))

    print(f"Loaded and chunked {len(chunks)} chunks from {len(pdf_paths)} PDF(s).")
    return chunks

# ---------------------------
# BM25 index builder & retriever
# ---------------------------
class BM25Retriever:
    def __init__(self, chunks: List[DocChunk]):
        self.chunks = chunks
        self.tokenized_texts = [simple_tokenize(c.page_content) for c in chunks]
        self.bm25 = BM25Okapi(self.tokenized_texts)

    def get_relevant_documents(self, query: str, k: int = 3) -> List[DocChunk]:
        q_tokens = simple_tokenize(query)
        if not q_tokens:
            return []
        scores = self.bm25.get_scores(q_tokens)
        idx_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        top = [i for i, sc in idx_scores[:k] if sc > 0]
        if not top and len(idx_scores) > 0:
            top = [i for i, _ in idx_scores[:k]]
        return [self.chunks[i] for i in top]

# ---------------------------
# Load docs and build BM25 index
# ---------------------------
print("📥 Ingesting PDFs and building BM25 index...")
chunks = load_and_chunk_pdfs(FILES_DIR)
retriever = BM25Retriever(chunks) if chunks else None
print("✅ BM25 index ready." if retriever else "❌ BM25 retriever not created (no chunks).")

# ---------------------------
# Define shared state schema for LangGraph
# ---------------------------
class ResearchState(TypedDict):
    topic: str
    summary: Optional[str]
    critique: Optional[str]
    insight: Optional[str]
    sources: Optional[List[str]]

# ---------------------------
# LangGraph agents using BM25 retriever
# ---------------------------
def researcher_agent(state: ResearchState):
    topic = state.get("topic", "").strip()
    if not topic:
        return {"summary": "No topic provided."}
    if not retriever:
        return {"summary": "No documents indexed for retrieval."}

    docs = retriever.get_relevant_documents(topic, k=4)
    if not docs:
        return {"summary": "No relevant documents found."}

    context_pieces = []
    sources = []
    for d in docs:
        snippet = d.page_content.strip()
        if len(snippet) > 800:
            snippet = snippet[:800].rsplit(" ", 1)[0] + " ..."
        source = d.metadata.get("source", "unknown")
        chunk_id = d.metadata.get("chunk_id", "")
        context_pieces.append(f"[SOURCE: {source} | CHUNK: {chunk_id}]\n{snippet}")
        sources.append(source)

    context = "\n\n---\n\n".join(context_pieces)
    prompt = (
        f"You are a research assistant. The user asked about: '{topic}'.\n\n"
        f"Read the following retrieved excerpts (lexical retrieval via BM25) and produce a concise summary "
        f"of the main findings or facts relevant to the topic. Be explicit about which sources support which points.\n\n"
        f"EXCERPTS:\n\n{context}\n\n"
        "Return a short summary and a short list of (source -> supporting sentence)."
    )
    resp = llm.invoke(prompt)
    summary_text = getattr(resp, "content", None) or str(resp)
    return {"summary": summary_text, "sources": list(dict.fromkeys(sources))}

def reviewer_agent(state: ResearchState):
    summary = state.get("summary", "")
    if not summary:
        return {"critique": "No summary to review."}
    prompt = (
        "You are a critical reviewer. Read the following summary and point out: "
        "1) statements that lack direct support from the provided excerpts, "
        "2) possible biases or missing considerations, and "
        "3) questions or follow-ups to verify the claims.\n\n"
        f"SUMMARY:\n\n{summary}\n\n"
        "Give your critique in bullet points."
    )
    resp = llm.invoke(prompt)
    critique_text = getattr(resp, "content", None) or str(resp)
    return {"critique": critique_text}

def synthesizer_agent(state: ResearchState):
    summary = state.get("summary", "")
    critique = state.get("critique", "")
    sources = state.get("sources", [])
    prompt = (
        "You are a synthesizer. Combine the summary and critique into a 'Collective Insight Report'. "
        "Include: a 2-3 sentence insight, 2 testable hypotheses or follow-up experiments, and which sources "
        "would be most relevant to test those hypotheses. Keep it concise.\n\n"
        f"SUMMARY:\n{summary}\n\nCRITIQUE:\n{critique}\n\nSOURCES:\n{', '.join(sources)}"
    )
    resp = llm.invoke(prompt)
    insight_text = getattr(resp, "content", None) or str(resp)
    return {"insight": insight_text}

# ---------------------------
# Create LangGraph pipeline
# ---------------------------
graph = StateGraph(ResearchState)
graph.add_node("researcher", researcher_agent)
graph.add_node("reviewer", reviewer_agent)
graph.add_node("synthesizer", synthesizer_agent)

graph.add_edge("researcher", "reviewer")
graph.add_edge("reviewer", "synthesizer")
graph.set_entry_point("researcher")
app = graph.compile()

# ---------------------------
# Interactive loop
# ---------------------------
def print_divider():
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    print("🤖 LangGraph (BM25) research lab ready.")
    if not retriever:
        print("Warning: No documents indexed. Add PDFs to 'files/' and rerun.")
    try:
        while True:
            topic = input("\nEnter a research topic (or 'exit' to quit): ").strip()
            if topic.lower() in ("exit", "quit"):
                break
            print("\nRunning agents pipeline (researcher -> reviewer -> synthesizer)...\n")
            result = app.invoke({"topic": topic})

            print_divider()
            print(f"Topic: {topic}\n")
            print("📘 Researcher Summary:\n")
            print(result.get("summary", "—"))
            print_divider()
            print("🔍 Reviewer Critique:\n")
            print(result.get("critique", "—"))
            print_divider()
            print("💡 Collective Insight:\n")
            print(result.get("insight", "—"))
            print_divider()
            print("📚 Sources used:", ", ".join(result.get("sources", [])))
            print_divider()
    except KeyboardInterrupt:
        print("\nExiting.")
