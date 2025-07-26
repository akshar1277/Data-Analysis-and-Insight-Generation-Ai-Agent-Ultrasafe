from crewai import Agent
import faiss, numpy as np
from sentence_transformers import SentenceTransformer

# build simple RAG KB at startup
model = SentenceTransformer("all-MiniLM-L6-v2")
with open("knowledge_base/stats_best_practices.txt") as f:
    docs = [l.strip() for l in f if l.strip()]
embs = model.encode(docs, convert_to_numpy=True)
index = faiss.IndexFlatIP(embs.shape[1])
index.add(embs)

def retrieve(query: str, k: int = 3):
    vec = model.encode([query], convert_to_numpy=True)
    sims, idx = index.search(vec, k)
    return [docs[i] for i in idx[0]]
