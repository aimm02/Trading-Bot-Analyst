import os
import pandas as pd
import ta
import requests
from Agent.state import AnalisisState

def ambil_kurs_idr():
    try:
        res = requests.get("https://open.er-api.com/v6/latest/USD", timeout=3).json()
        return float(res['rates']['IDR'])
    except:
        return 16200.0 # Nilai fallback estimasi

def agen_risk(state: AnalisisState):
    if state["data_history_status"] == "GAGAL":
        return {
            "harga_masuk": 0.0, "arah_posisi": "TIDAK ADA", "stop_loss": 0.0,
            "take_profit": 0.0, "atr": 0.0, "kurs_usd_idr": 0.0,
            "saran_alokasi_idr": 0.0, "jumlah_koin": 0.0
        }
        
    simbol = state["simbol_koin"]
    kesimpulan = state["kesimpulan_akhir"].upper()
    
    print(f"-> [Agen Risk] Menghitung Risiko Volatilitas ATR & Ukuran Posisi Modal...")
    file_history = os.path.join("Data", "History", f"{simbol}_1jam.csv")
    
    try:
        df = pd.read_csv(file_history, index_col=0, parse_dates=True)
        harga_terkini = float(df['Close'].iloc[-1])
        
        # 1. Hitung ATR Dinamis (Periode 14)
        atr_ind = ta.volatility.AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14)
        df['atr'] = atr_ind.average_true_range()
        atr_val = float(df['atr'].iloc[-1])
        
        kurs_idr = ambil_kurs_idr()
        
        # Parameter Portofolio Standar (Dapat disesuaikan)
        MODAL_PORTOFOLIO_IDR = 10_000_000.0  # Asumsi modal trading Rp 10 Juta
        RISIKO_PER_TRADE_PERSEN = 0.01       # Maksimal toleransi rugi 1% (Rp 100.000)
        toleransi_rugi_idr = MODAL_PORTOFOLIO_IDR * RISIKO_PER_TRADE_PERSEN
        
        arah = "HOLD (TIDAK ADA POSISI)"
        stop_loss = 0.0
        take_profit = 0.0
        saran_masuk_idr = 0.0
        jumlah_koin = 0.0
        
        if "BUY" in kesimpulan and "OVERHEATED LONG" not in state.get("status_derivatif", ""):
            arah = "LONG (BELI)"
            stop_loss = harga_terkini - (1.5 * atr_val)  # Jarak SL berbasis ATR
            take_profit = harga_terkini + (3.0 * atr_val) # Target TP Risk:Reward 1:2
            
            jarak_risiko_usd = harga_terkini - stop_loss
            jarak_risiko_idr = jarak_risiko_usd * kurs_idr
            
            if jarak_risiko_idr > 0:
                jumlah_koin = toleransi_rugi_idr / jarak_risiko_idr
                saran_masuk_idr = jumlah_koin * (harga_terkini * kurs_idr)
                
        elif "SELL" in kesimpulan:
            arah = "SHORT (JUAL)"
            stop_loss = harga_terkini + (1.5 * atr_val)
            take_profit = harga_terkini - (3.0 * atr_val)
            
            jarak_risiko_usd = stop_loss - harga_terkini
            jarak_risiko_idr = jarak_risiko_usd * kurs_idr
            
            if jarak_risiko_idr > 0:
                jumlah_koin = toleransi_rugi_idr / jarak_risiko_idr
                saran_masuk_idr = jumlah_koin * (harga_terkini * kurs_idr)
                
        return {
            "harga_masuk": harga_terkini,
            "arah_posisi": arah,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "atr": atr_val,
            "kurs_usd_idr": kurs_idr,
            "saran_alokasi_idr": saran_masuk_idr,
            "jumlah_koin": jumlah_koin
        }
        
    except Exception as e:
        print(f"   [!] Galat Agen Risk: {e}")
        return {
            "harga_masuk": 0.0, "arah_posisi": "ERROR", "stop_loss": 0.0,
            "take_profit": 0.0, "atr": 0.0, "kurs_usd_idr": 0.0,
            "saran_alokasi_idr": 0.0, "jumlah_koin": 0.0
        }