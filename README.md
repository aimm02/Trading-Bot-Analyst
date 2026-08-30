# Quantitative Crypto Market Analyst & Signal Engine

An autonomous, multi-agent quantitative cryptocurrency market intelligence and advisory system built with LangGraph, Google Gemini, and algorithmic technical indicators. 

Designed strictly as a non-execution, analytical engine, this platform continuously monitors crypto asset pairs, evaluates multi-timeframe structural trends, processes macroeconomic sentiment, computes directional probabilities, and calculates volatility-adjusted risk levels (ATR). Actionable trading setups meeting strict statistical confidence thresholds are instantly dispatched to Telegram.

---

## Technology Stack

### Programming Language & Runtime
* **Python 3.10+**: Core runtime environment.

### Multi-Agent Orchestration
* **LangGraph (`langgraph`)**: Deterministic state machine and directed acyclic graph (DAG) execution framework via `StateGraph` for structured inter-agent data passing.

### Artificial Intelligence & Reasoning
* **Google GenAI SDK (`google-genai`)**: Integration with Gemini 2.5 Flash for multimodal technical synthesis, candlestick pattern context confirmation, and headline sentiment analysis.

### Quantitative Analysis & Mathematics
* **Pandas & NumPy**: Vectorized operations, time-series data cleansing, resampling, and OHLCV matrix calculations.
* **Technical Analysis Library (`ta`)**: Mathematical computation of core momentum, volatility, and trend indicators including Exponential Moving Averages (EMA), Relative Strength Index (RSI), and Average True Range (ATR).

### Market Data Ingestion
* **Twelve Data REST API**: Primary low-latency real-time 1-minute and 15-minute candlestick data feed.
* **Yahoo Finance (`yfinance`)**: Secondary fallback feed ensuring uninterrupted historical time-series retrieval during API rate limits.

### Distribution & Operational Alerting
* **Telegram Bot API**: Programmatic delivery of structured market intelligence reports, trade parameters, and risk sizing via HTTPS POST.

### Environment & Utilities
* **Python-Dotenv**: Environment variable isolation and secure credential management.

---

## Core Characteristics

* **Pure Advisory Architecture:** Zero order execution risk. The system does not interface with exchange execution endpoints or private trading keys, focusing strictly on data integrity, anomaly detection, and probability quantification.
* **Dual-Timeframe Quantitative Confluence:**
  * **15-Minute (15M) Regime Filter:** Identifies overarching trend structure relative to the 50-period Exponential Moving Average (EMA 50).
  * **1-Minute (1M) Execution Momentum:** Validates short-term momentum triggers via EMA 9/21 crossovers and Fast RSI (9) mean-reversion boundaries.
* **Dynamic Volatility & Risk Sizing:** Invalidation levels (Stop Loss), profit targets (Take Profit), and position allocations are calculated dynamically using the 14-period Average True Range (ATR), adapting automatically to shifting market volatility.
* **Threshold-Gated Dispatch:** Intelligence alerts are triggered only when the quantitative model reaches a confidence score of 60% or higher, eliminating low-probability market noise.

---

## System Workflow

```text
               +-------------------------------------------------+
               |             Market Data Ingestion               |
               |       (Twelve Data API / Yahoo Finance)         |
               +-------------------------------------------------+
                                        |
                                        v
+------------------+         +---------------------+         +---------------------+
|  History Agent   | ------> |     Macro Agent     | ------> |   Technical Agent   |
|  Fetches 1M/15M  |         |  Scans & Analyzes   |         |  TA Computation &   |
|  OHLCV Datasets  |         |  News Sentiment     |         |  Gemini Synthesis   |
+------------------+         +---------------------+         +---------------------+
                                                                        |
                                                                        v
+------------------+                                         +---------------------+
|   Notify Agent   | <-------------------------------------- |     Risk Agent      |
|  Dispatches to   |           (If Probability >= 60%)       |  Calculates ATR,    |
|  Telegram Bot    |                                         |  SL, TP & Sizing    |
+------------------+                                         +---------------------+
