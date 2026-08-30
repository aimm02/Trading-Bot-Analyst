import os
import yfinance as yf
import pandas as pd
from Agent.state import AnalisisState

def agen_history(state: AnalisisState):
    simbol = state["simbol_koin"]
    ticker = state["ticker_yf"]
    print(f"\n-> [Agen History] Mengunduh data Multi-Timeframe (1D, 4H, 1H) untuk {simbol}...")
    
    folder_history = os.path.join("Data", "History")
    os.makedirs(folder_history, exist_ok=True)
    
    try:
        koin_data = yf.Ticker(ticker)
        
        # 1. Unduh Data Harian (1D) untuk Tren Makro (1 Tahun)
        df_1d = koin_data.history(period="1y", interval="1d")
        if df_1d.empty:
            raise ValueError(f"Data 1D untuk {ticker} tidak ditemukan.")
        df_1d.to_csv(os.path.join(folder_history, f"{simbol}_1hari.csv"))
        
        # 2. Unduh Data 1 Jam (1H) untuk Pemicu Eksekusi (60 Hari)
        df_1h = koin_data.history(period="60d", interval="1h")
        if df_1h.empty:
            raise ValueError(f"Data 1H untuk {ticker} tidak ditemukan.")
        df_1h.to_csv(os.path.join(folder_history, f"{simbol}_1jam.csv"))
        
        # 3. Resample Data 1H Menjadi Kandel 4 Jam (4H) untuk Struktur Pasar
        df_4h = df_1h.resample('4h').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        df_4h.to_csv(os.path.join(folder_history, f"{simbol}_4jam.csv"))
        
        print(f"   [+] Berhasil mengunduh & menyusun dataset 1D, 4H, dan 1H.")
        return {"data_history_status": "BERHASIL"}
        
    except Exception as e:
        print(f"\n[!] Galat Agen History: {e}")
        return {"data_history_status": "GAGAL"}