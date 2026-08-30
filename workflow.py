from langgraph.graph import StateGraph, END

from Agent.state import AnalisisState
from Agent.agent_history import agen_history
from Agent.agent_news import agen_news
from Agent.agent_derivatives import agen_derivatives
from Agent.agent_technical import agen_teknikal
from Agent.agent_risk import agen_risk
from Agent.agent_logger import agen_logger
from Agent.agent_notify import agen_notify

def bangun_grafik():
    print("[Sistem] Merakit grafik LangGraph dengan Notifikasi Telegram...")
    workflow = StateGraph(AnalisisState)

    workflow.add_node("history", agen_history)
    workflow.add_node("news", agen_news)
    workflow.add_node("derivatives", agen_derivatives)
    workflow.add_node("teknikal", agen_teknikal)
    workflow.add_node("risk", agen_risk)
    workflow.add_node("logger", agen_logger)
    workflow.add_node("notify", agen_notify)

    workflow.set_entry_point("history")
    workflow.add_edge("history", "news")
    workflow.add_edge("news", "derivatives")
    workflow.add_edge("derivatives", "teknikal")
    workflow.add_edge("teknikal", "risk")
    workflow.add_edge("risk", "logger")
    workflow.add_edge("logger", "notify")
    workflow.add_edge("notify", END)

    return workflow.compile()

app_graph = bangun_grafik()