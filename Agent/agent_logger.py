import os
import sqlite3
from datetime import datetime
from Agent.state import AnalisisState

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            simbol TEXT,
            arah_posisi TEXT,
            harga_masuk REAL,
            stop_loss REAL,
            take_profit REAL,
            atr REAL,
            saran_idr REAL,
            skor_sentimen REAL,
            funding_rate REAL,
            status_eksekusi TEXT
        )
    """)
    conn.commit()
    conn.close()

def agen_logger(state: AnalisisState):
    if state["data_history_status"] == "GAGAL":
        return {}
        
    print(f"-> [Agen Logger] Mencatat sinyal trading ke Database SQLite...")
    os.makedirs("Data", exist_ok=True)
    db_path = os.path.join("Data", "trading_signals.db")
    init_db(db_path)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO signals (
                timestamp, simbol, arah_posisi, harga_masuk, stop_loss,
                take_profit, atr, saran_idr, skor_sentimen, funding_rate, status_eksekusi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            state["simbol_koin"],
            state["arah_posisi"],
            state["harga_masuk"],
            state["stop_loss"],
            state["take_profit"],
            state["atr"],
            state["saran_alokasi_idr"],
            state["skor_sentimen"],
            state["funding_rate"],
            "LOGGED"
        ))
        conn.commit()
        conn.close()
        print(f"   [+] Sinyal berhasil diarsipkan di '{db_path}'.")
    except Exception as e:
        print(f"   [!] Galat Agen Logger: {e}")
        
    return {}