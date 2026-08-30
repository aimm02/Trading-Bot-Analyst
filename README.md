# Quantitative Crypto Market Analyst & Signal Engine

Sistem analisis pasar kripto kuantitatif berbasis *multi-agent architecture* menggunakan **LangGraph**, **Google Gemini**, dan **Technical Indicators**. Sistem ini dirancang khusus untuk memantau pasar kripto secara non-eksekusi (*pure advisory/intelligence*): melakukan evaluasi struktur tren multi-timeframe, mengukur sentimen, menghitung probabilitas arah pasar secara matematis, menyusun kalkulasi manajemen risiko dinamis berbasis volatilitas (ATR), serta mendistribusikan sinyal transaksi presisi langsung ke Telegram.

---

## Karakteristik Sistem

- **Pure Analytical & Non-Execution:** Sistem tidak terhubung ke API eksekusi broker maupun bursa berjangka. Fokus diarahkan penuh pada pemrosesan data, identifikasi setup, dan validasi probabilitas tanpa risiko operasional order placement.
- **Multi-Agent Orchestration (LangGraph):** Setiap tahap analisis didelegasikan ke modul agen independen dalam rantai terstruktur.
- **Dual-Timeframe Quantitative Confluence:**
  - **15-Menit (15M):** Filter arah tren makro menggunakan Exponential Moving Average (EMA 50).
  - **1-Menit (1M):** Pemicu momentum mikro menggunakan persilangan cepat EMA 9/21 dan Fast RSI (9).
- **Dynamic Volatility & Risk Sizing:** Penentuan level Invalidation (Stop Loss), Target (Take Profit), dan batas nominal risiko per transaksi dihitung matematis berdasarkan Average True Range (ATR 14).
- **Automated Intelligence Dispatch:** Pengiriman notifikasi sinyal hanya dipicu jika model menghasilkan tingkat keyakinan (confidence score) di atas ambang batas (>= 60%).

---

## Arsitektur Pipeline

```text
[History Agent] ➔ [Macro Agent] ➔ [Technical Agent] ➔ [Risk Agent] ➔ [Notify Agent]
