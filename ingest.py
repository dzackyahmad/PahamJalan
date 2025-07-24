from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Load dokumen
with open("master_lalu_lintas.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
texts = text_splitter.split_text(text)

# Embedding lokal (gratis)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_texts(texts, embeddings, persist_directory="db")
db.persist()
