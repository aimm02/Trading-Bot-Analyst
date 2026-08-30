from typing import TypedDict

class AnalisisState(TypedDict):
    simbol_koin: str
    ticker_yf: str
    data_history_status: str
    teks_berita: str
    sinyal_teknikal: str
    skor_sentimen: float
    kesimpulan_akhir: str
    funding_rate: float
    open_interest: str
    status_derivatif: str
    harga_masuk: float
    arah_posisi: str
    stop_loss: float
    take_profit: float
    atr: float
    kurs_usd_idr: float
    saran_alokasi_idr: float
    jumlah_koin: float