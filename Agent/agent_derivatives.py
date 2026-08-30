import requests
import urllib3
from Agent.state import AnalisisState

# Nonaktifkan peringatan SSL tidak aman jika menggunakan verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def agen_derivatives(state: AnalisisState):
    if state["data_history_status"] == "GAGAL":
        return {"funding_rate": 0.0, "open_interest": "N/A", "status_derivatif": "TIDAK TERSEDIA"}
        
    simbol = state["simbol_koin"]
    ticker_futures = f"{simbol}USDT"
    print(f"\n-> [Agen Derivatif] Memeriksa Likuiditas & Funding Rate untuk {ticker_futures}...")
    
    funding_rate = 0.0
    oi_formatted = "N/A"
    status_deriv = "NETRAL"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    # 1. Coba Tarik dari Bybit V5 API (Aman dari blokir ISP lokal)
    try:
        url_bybit = f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={ticker_futures}"
        res = requests.get(url_bybit, headers=headers, timeout=5, verify=False).json()
        
        if res.get("retCode") == 0 and res["result"]["list"]:
            data = res["result"]["list"][0]
            funding_rate = float(data.get("fundingRate", 0.0)) * 100
            oi_val = float(data.get("openInterest", 0.0))
            oi_formatted = f"{oi_val:,.0f} {simbol}"
            
            if funding_rate > 0.04:
                status_deriv = "OVERHEATED LONG (Risiko Long Squeeze Tinggi)"
            elif funding_rate < -0.03:
                status_deriv = "HEAVY SHORT (Peluang Short Squeeze)"
            else:
                status_deriv = "LIKUIDITAS NORMAL / NETRAL"
                
            print(f"   [+] Data Bybit -> Funding Rate: {funding_rate:.4f}% | OI: {oi_formatted} | Status: {status_deriv}")
            return {
                "funding_rate": funding_rate,
                "open_interest": oi_formatted,
                "status_derivatif": status_deriv
            }
    except Exception:
        pass

    # 2. Fallback ke Binance Futures API (dengan bypass SSL)
    try:
        url_fr = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={ticker_futures}&limit=1"
        res_fr = requests.get(url_fr, headers=headers, timeout=4, verify=False).json()
        if isinstance(res_fr, list) and len(res_fr) > 0:
            funding_rate = float(res_fr[0]["fundingRate"]) * 100
            
        url_oi = f"https://fapi.binance.com/fapi/v1/openInterest?symbol={ticker_futures}"
        res_oi = requests.get(url_oi, headers=headers, timeout=4, verify=False).json()
        if "openInterest" in res_oi:
            oi_val = float(res_oi["openInterest"])
            oi_formatted = f"{oi_val:,.0f} {simbol}"
            
        if funding_rate > 0.04:
            status_deriv = "OVERHEATED LONG (Risiko Long Squeeze)"
        elif funding_rate < -0.03:
            status_deriv = "HEAVY SHORT (Peluang Short Squeeze)"
        else:
            status_deriv = "LIKUIDITAS NORMAL / NETRAL"
            
        print(f"   [+] Data Binance -> Funding Rate: {funding_rate:.4f}% | OI: {oi_formatted}")
        
    except Exception as e:
        print(f"   [!] Info Derivatif: Pasar derivatif tidak ditemukan ({e}).")
        status_deriv = "DATA DERIVATIF TIDAK TERSEDIA"
        
    return {
        "funding_rate": funding_rate,
        "open_interest": oi_formatted,
        "status_derivatif": status_deriv
    }