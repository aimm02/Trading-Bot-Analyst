import os
import feedparser
from google import genai
from dotenv import load_dotenv
from Agent.state import AnalisisState

def agen_news(state: AnalisisState):
    if state["data_history_status"] == "GAGAL":
        return {"teks_berita": "Gagal melanjutkan karena data harga tidak ada.", "skor_sentimen": 0.0}
        
    simbol = state["simbol_koin"]
    print(f"\n-> [Agen News] Mencari berita terbaru {simbol}...")
    
    folder_news = os.path.join("Data", "News")
    os.makedirs(folder_news, exist_ok=True)
    
    try:
        url_feed = f"https://finance.yahoo.com/rss/headline?s={state['ticker_yf']}"
        feed = feedparser.parse(url_feed)
        
        berita = []
        for entry in feed.entries[:7]: 
            berita.append(f"- {entry.title}")
            
        teks_berita = "\n".join(berita) if berita else f"Tidak ditemukan berita signifikan untuk {simbol}."
        
        nama_file_berita = os.path.join(folder_news, f"{simbol}_berita_terbaru.txt")
        with open(nama_file_berita, "w", encoding="utf-8") as f:
            f.write(teks_berita)
            
        print(f"\nBerita ditemukan dan diarsipkan di '{nama_file_berita}'.")
        
        # Coba panggil Gemini untuk analisis sentimen
        load_dotenv()
        klien = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        prompt = f"""
        Evaluasi sentimen pasar dari berita terbaru terkait {simbol} berikut:
        {teks_berita}
        Apakah berita-berita ini berpotensi menaikkan (Bullish) atau menurunkan (Bearish) harga?
        Berikan HANYA SATU ANGKA desimal antara -1.0 (Sangat Bearish) hingga 1.0 (Sangat Bullish). Jangan tulis teks apa pun selain angka.
        """
        respons = klien.models.generate_content(model='gemini-3.6-flash', contents=prompt)
        skor = float(respons.text.strip())
        print(f"\nSkor Sentimen LLM: {skor}")
        
        return {"teks_berita": teks_berita, "skor_sentimen": skor}
        
    except Exception as e:
        # PENGAMAN (FALLBACK): Jika kuota habis (429) atau error lain, berikan skor aman 0.0
        print(f"\n[!] Peringatan Agen News (AI Terbatas/Habis): Menggunakan nilai sentimen netral (0.0). Detail: {e}")
        return {"teks_berita": teks_berita if 'teks_berita' in locals() else "Gagal menarik berita.", "skor_sentimen": 0.0}