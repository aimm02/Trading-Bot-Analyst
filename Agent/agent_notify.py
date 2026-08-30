import os
import requests
from dotenv import load_dotenv
from Agent.state import AnalisisState

def agen_notify(state: AnalisisState):
    if state.get("data_history_status") == "GAGAL":
        return {}

    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("\n-> [Agen Notify] Kredensial Telegram tidak ditemukan di .env. Notifikasi dilewati.")
        return {}

    simbol = state["simbol_koin"]
    print(f"\n-> [Agen Notify] Mengirim laporan kuantitatif {simbol} ke Telegram...")

    pesan = (
        f"<b>LAPORAN SINYAL KUANTITATIF: {simbol}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Rekomendasi Posisi:</b> {state['arah_posisi']}\n"
        f"<b>Harga Masuk:</b> ${state['harga_masuk']:,.4f}\n"
        f"<b>Stop Loss:</b> ${state['stop_loss']:,.4f}\n"
        f"<b>Take Profit:</b> ${state['take_profit']:,.4f}\n"
        f"<b>Volatilitas ATR:</b> ${state['atr']:,.4f}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Alokasi Modal (IDR):</b>\n"
        f"Saran Beli: <b>Rp {state['saran_alokasi_idr']:,.0f}</b>\n"
        f"Jumlah Koin: {state['jumlah_koin']:.4f} {simbol}\n"
        f"Kurs Acuan: Rp {state['kurs_usd_idr']:,.0f}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Metrik Pasar & Derivatif:</b>\n"
        f"• Sentimen: {state['skor_sentimen']}\n"
        f"• Funding Rate: {state['funding_rate']:.4f}%\n"
        f"• Likuiditas: {state['status_derivatif']}\n"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": pesan,
        "parse_mode": "HTML"
    }

    try:
        res = requests.post(url, json=payload, timeout=8)
        if res.status_code == 200:
            print("   [+] Notifikasi Telegram berhasil dikirim.")
        else:
            print(f"   [!] Gagal mengirim pesan Telegram: {res.text}")
    except Exception as e:
        print(f"   [!] Galat Agen Notify: {e}")

    return {}