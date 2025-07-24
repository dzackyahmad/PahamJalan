from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langdetect import detect
from deep_translator import GoogleTranslator

# Setup FastAPI
app = FastAPI()

# CORS: biar bisa diakses dari browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Vector DB dan Model
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="db", embedding_function=embedding)
retriever = db.as_retriever()
llm = OllamaLLM(model="mistral:7b", temperature=0.3)

# Prompt template untuk chatbot
prompt = PromptTemplate.from_template("""
Anda adalah chatbot hukum lalu lintas Indonesia.

📌 Tugas Anda adalah menjawab **pertanyaan hukum lalu lintas** berdasarkan:
- Undang-Undang No. 22 Tahun 2009
- Peraturan Pemerintah (PP)
- Peraturan Menteri Perhubungan (Permenhub)
- Buku resmi atau panduan dari pemerintah Indonesia

📌 Anda **WAJIB menjawab dalam Bahasa Indonesia**.
📌 Jika pertanyaan **tidak relevan**, Anda **HARUS menolak dengan sopan**. Balas dengan:
"Maaf, saya hanya bisa menjawab seputar hukum lalu lintas dan angkutan jalan di Indonesia."

---

🧠 Contoh pertanyaan **valid**:
- Apa isi Pasal 77 UU No. 22 Tahun 2009?
- Apa sanksi jika tidak memiliki SIM?
- Permenhub No. 17 Tahun 2021 mengatur tentang apa?
- Apakah motor listrik wajib bayar pajak?
- Apa arti marka kuning di jalan?

🚫 Contoh pertanyaan **tidak valid (OOT)**:
- Siapa presiden Indonesia sekarang?
- Apa itu revolusi industri?
- Buatkan puisi tentang lalu lintas
- Bagaimana cara mengendarai mobil manual?
- Berapa harga mobil listrik?

---

📌 Format jawaban yang HARUS digunakan:

📌 Jawaban:
- [Jawaban langsung pada poin penting]
- [Gunakan poin-poin untuk memisahkan informasi]
- [Jangan gunakan paragraf panjang yang melelahkan untuk dibaca]
- [Gunakan bahasa yang mudah dimengerti, hindari jargon hukum yang rumit]

📚 Referensi / Dasar Hukum:
- [Sebutkan nama UU/PP/Permenhub, Pasal dan Ayat jika ada]
- [Gunakan format seperti: "UU No. 22 Tahun 2009, Pasal 77 Ayat (1)"]

---

📨 Pertanyaan Pengguna:
{question}

📄 Informasi Pendukung (gunakan hanya jika relevan):
{context}
""")

# Model pertanyaan dari user
class Question(BaseModel):
    question: str

# Endpoint utama chatbot
@app.post("/ask")
async def ask_bot(data: Question):
    docs = retriever.get_relevant_documents(data.question)
    context = "\n\n".join(doc.page_content for doc in docs)
    final_prompt = prompt.format(context=context, question=data.question)
    result = llm.invoke(final_prompt)

    # Auto translate kalau masih Bahasa Inggris
    if detect(result) == "en":
        result = GoogleTranslator(source='en', target='id').translate(result)

    return {"answer": result}
