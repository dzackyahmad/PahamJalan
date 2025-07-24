# PahamJalan 🚦

**PahamJalan** adalah chatbot hukum lalu lintas Indonesia yang dapat menjawab pertanyaan berdasarkan:
- UU No. 22 Tahun 2009
- Peraturan Pemerintah
- Peraturan Menteri Perhubungan
- Buku resmi atau panduan dari pemerintah

Chatbot ini dibangun menggunakan:
- [LangChain](https://www.langchain.com/)
- [Ollama](https://ollama.com/)
- Model lokal seperti Mistral
- ChromaDB sebagai vectorstore
- Frontend HTML/CSS/JS sederhana

---

## 🔧 Cara Menjalankan Secara Lokal

### 1. Clone Repository
```bash
git clone https://github.com/dzackyahmad/PahamJalan.git
cd PahamJalan
```

### 2. Buat Virtual Environment dan Install Dependency
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# atau
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## 📄 3. Siapkan Dataset

Letakkan semua file PDF peraturan di folder `dataset/`, misalnya:
- `UU_Nomor_22_2009.pdf`
- `PP_Nomor_30_2021.pdf`
- `Permenhub_No_17_2021.pdf`
- `BUKU_TATA_CARA_BERLALULINTAS.pdf`

---

### 4. Convert PDF ke Teks
```bash
python converter.py
```

---

### 5. Lakukan Ingest ke Vector DB
```bash
python ingest.py
```

---

### 6. Jalankan Server Chatbot (Backend)
```bash
python app.py
```
Server akan aktif di http://localhost:8000

---

## 🌐 Hosting Secara Publik (Frontend + Ngrok)

### Frontend
- Upload `index.html`, `style.css`, `script.js`, dan aset gambar ke GitHub
- Aktifkan GitHub Pages dari repositori tersebut

### Backend
Gunakan [Ngrok](https://ngrok.com/) agar backend lokal dapat diakses publik:
```bash
ngrok http 8000
```
Ganti URL di `script.js` agar mengarah ke URL dari Ngrok (`https://xxxx.ngrok.io/ask`)

---

## 👨‍💻 Tim Pengembang

PahamJalan dibuat oleh:
- Hafizh Fadhl Muhammad
- Dzacky Ahmad
- Farhan Zia Rizky

---

## 📜 Lisensi

MIT License