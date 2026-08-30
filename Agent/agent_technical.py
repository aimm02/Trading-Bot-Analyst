import os
import pandas as pd
import ta
from google import genai
from dotenv import load_dotenv
from Agent.state import AnalisisState

def agen_teknikal(state: AnalisisState):
    if state["data_history_status"] == "GAGAL":
        return {"sinyal_teknikal": "TIDAK VALID", "kesimpulan_akhir": "Proses dibatalkan karena data riwayat gagal dimuat."}
        
    simbol = state["simbol_koin"]
    print(f"-> [Agen Teknikal] Memproses Analisis Multi-Timeframe (1D -> 4H -> 1H)...")
    
    folder = os.path.join("Data", "History")
    
    try:
        # 1. Baca dan hitung Indikator 1D (Filter Makro)
        df_1d = pd.read_csv(os.path.join(folder, f"{simbol}_1hari.csv"), index_col=0, parse_dates=True)
        ema_200_1d = ta.trend.EMAIndicator(close=df_1d['Close'], window=200).ema_indicator().iloc[-1]
        close_1d = df_1d['Close'].iloc[-1]
        tren_makro_1d = "BULLISH (Di atas EMA 200)" if close_1d > ema_200_1d else "BEARISH (Di bawah EMA 200)"
        
        # 2. Baca dan hitung Indikator 4H (Struktur Pasar)
        df_4h = pd.read_csv(os.path.join(folder, f"{simbol}_4jam.csv"), index_col=0, parse_dates=True)
        ema_50_4h = ta.trend.EMAIndicator(close=df_4h['Close'], window=50).ema_indicator().iloc[-1]
        rsi_4h = ta.momentum.RSIIndicator(close=df_4h['Close'], window=14).rsi().iloc[-1]
        
        # 3. Baca dan hitung Indikator 1H (Trigger Eksekusi)
        df_1h = pd.read_csv(os.path.join(folder, f"{simbol}_1jam.csv"), index_col=0, parse_dates=True)
        df_1h['ema_50'] = ta.trend.EMAIndicator(close=df_1h['Close'], window=50).ema_indicator()
        df_1h['ema_200'] = ta.trend.EMAIndicator(close=df_1h['Close'], window=200).ema_indicator()
        df_1h['rsi'] = ta.momentum.RSIIndicator(close=df_1h['Close'], window=14).rsi()
        
        macd_ind = ta.trend.MACD(close=df_1h['Close'])
        macd_1h = macd_ind.macd().iloc[-1]
        macd_sig_1h = macd_ind.macd_signal().iloc[-1]
        
        harga_terkini = df_1h['Close'].iloc[-1]
        ema_50_1h = df_1h['ema_50'].iloc[-1]
        ema_200_1h = df_1h['ema_200'].iloc[-1]
        rsi_1h = df_1h['rsi'].iloc[-1]
        
        ringkasan_mtf = f"""
        Ringkasan Multi-Timeframe {simbol}:
        - 1D (Makro): Harga ${close_1d:.2f} vs EMA 200 (${ema_200_1d:.2f}) -> Status: {tren_makro_1d}
        - 4H (Struktur): EMA 50 (${ema_50_4h:.2f}), RSI 4H ({rsi_4h:.1f})
        - 1H (Trigger): Harga ${harga_terkini:.2f}, EMA 50 (${ema_50_1h:.2f}), EMA 200 (${ema_200_1h:.2f}), RSI 1H ({rsi_1h:.1f}), MACD ({macd_1h:.4f} vs Sig {macd_sig_1h:.4f})
        - Sentimen Berita: {state['skor_sentimen']}
        """
        
        try:
            load_dotenv()
            klien = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            prompt = f"""
            Anda adalah Analis Kripto Kuantitatif. Evaluasi data Multi-Timeframe berikut:
            {ringkasan_mtf}
            
            Aturan Hierarki:
            - Hanya rekomendasikan BUY jika tren 1D Bullish dan 1H memberikan sinyal beli.
            - Hanya rekomendasikan SELL jika tren 1D Bearish dan 1H memberikan sinyal jual.
            - Jika tren bertentangan, wajib pilih HOLD / WAIT FOR PULLBACK.
            
            Format Output:
            [STATUS TREN MTF]: (Sebutkan keselarasan 1D, 4H, dan 1H)
            [ANALISIS MENDALAM]: (Penjelasan alasan)
            [REKOMENDASI]: (BUY / SELL / HOLD)
            """
            respons = klien.models.generate_content(model='gemini-3.6-flash', contents=prompt)
            analisis_ai = respons.text.strip()
            print("   [+] Analisis Multi-Timeframe AI Selesai.")
            
        except Exception as ai_err:
            print(f"   [!] Peringatan: Kuota AI habis, menggunakan evaluasi MTF otomatis. ({ai_err})")
            
            # Logika Fallback Matematika Multi-Timeframe
            if close_1d > ema_200_1d and ema_50_1h > ema_200_1h and rsi_1h < 68:
                rekomendasi = "BUY"
                status_mtf = "BULLISH ALIGNED (1D Makro Uptrend & 1H Trigger Valid)"
                alasan = f"Tren makro harian mengonfirmasi kenaikan (di atas EMA 200). Grafik 1 jam selaras dengan EMA 50 di atas EMA 200 dan RSI {rsi_1h:.1f} berada pada momentum sehat."
            elif close_1d < ema_200_1d and ema_50_1h < ema_200_1h and rsi_1h > 32:
                rekomendasi = "SELL"
                status_mtf = "BEARISH ALIGNED (1D Makro Downtrend & 1H Trigger Valid)"
                alasan = f"Tren makro harian berada dalam tekanan jual. Grafik 1 jam mengonfirmasi kelanjutan penurunan harga."
            else:
                rekomendasi = "HOLD"
                status_mtf = "MTF CONFLICT / RANGING (Tren Tidak Selaras)"
                alasan = f"Struktur grafik makro (1D) dan grafik operasional (1H) saling bertentangan atau berada di area konsolidasi. Disarankan menunggu konfirmasi tren berikutnya."
                
            analisis_ai = f"[STATUS TREN MTF]: {status_mtf}\n[ANALISIS MENDALAM]: {alasan}\n[REKOMENDASI]: {rekomendasi}"
            
        return {
            "sinyal_teknikal": f"1D: {tren_makro_1d} | 1H: ${harga_terkini:.4f} (RSI: {rsi_1h:.1f})",
            "kesimpulan_akhir": analisis_ai
        }
        
    except Exception as e:
        print(f"\n[!] Galat Agen Teknikal: {e}")
        return {"sinyal_teknikal": "ERROR", "kesimpulan_akhir": f"Gagal merumuskan analisis: {e}"}