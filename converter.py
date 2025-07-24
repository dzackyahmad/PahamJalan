import fitz  # PyMuPDF
import os

# Daftar file PDF dan judulnya
files = [
    ("dataset/UU_Nomor_22_2009.pdf", "UU No.22 Tahun 2009"),
    ("dataset/PP_Nomor_30_2021.pdf", "PP No.30 Tahun 2021"),
    ("dataset/Permenhub_No_17_2021.pdf", "Permenhub No.17 Tahun 2021"),
    ("dataset/BUKU_TATA_CARA_BERLALULINTAS.pdf", "BUKU Tata Cara Berlalu Lintas"),
]

# Path output
output_path = "master_lalu_lintas.txt"

# Fungsi konversi PDF ke teks
def convert_pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# Mulai konversi dan gabungkan semua
with open(output_path, "w", encoding="utf-8") as outfile:
    for path, title in files:
        print(f"🔄 Mengonversi: {title}")
        try:
            text = convert_pdf_to_text(path)
            outfile.write(f"\n\n=== {title} ===\n\n{text}\n\n")
        except Exception as e:
            print(f"❌ Gagal membaca {path}: {e}")

print(f"\n✅ Semua selesai! Hasil disimpan di: {output_path}")
