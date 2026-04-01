"""
總經引擎 — FRED 景氣象限判定
象限：🟢擴張 / 🔵復甦 / 🟡過熱 / 🔴衰退
"""
import os
import streamlit as st
from utils.fetcher import get_fred

FRED_KEY = os.environ.get("FRED_API_KEY", "")

# FRED 系列代碼
SERIES = {
    "fed_rate":    "FEDFUNDS",   # 聯邦基金利率
    "cpi_yoy":     "CPIAUCSL",   # CPI（需計算 YoY）
    "unemployment":"UNRATE",     # 失業率
    "yield_10y":   "GS10",       # 10 年期公債殖利率
    "yield_2y":    "GS2",        # 2 年期公債殖利率
}


@st.cache_data(ttl=3600)
def get_macro_phase() -> dict:
    """
    抓取 FRED 數據並判定景氣象限。
    回傳 dict:
      {
        "phase": "擴張" | "復甦" | "過熱" | "衰退",
        "emoji": "🟢" | "🔵" | "🟡" | "🔴",
        "allocation": {"股": int, "債": int},
        "indicators": {series_id: latest_value},
        "updated_at": str,
      }
    """
    if not FRED_KEY:
        return _fallback()

    indicators = {}
    for name, sid in SERIES.items():
        s = get_fred(sid, FRED_KEY)
        indicators[name] = round(float(s.iloc[-1]), 2) if not s.empty else None

    phase, emoji, alloc = _classify(indicators)
    from datetime import datetime
    return {
        "phase": phase,
        "emoji": emoji,
        "allocation": alloc,
        "indicators": indicators,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def _classify(ind: dict) -> tuple[str, str, dict]:
    """根據指標判定象限（簡化規則）。"""
    rate = ind.get("fed_rate") or 0
    unemp = ind.get("unemployment") or 5
    cpi = ind.get("cpi_yoy") or 2
    spread = (ind.get("yield_10y") or 3) - (ind.get("yield_2y") or 2)

    if spread < 0:                          # 殖利率倒掛 → 衰退警告
        return "衰退", "🔴", {"股": 30, "債": 70}
    if unemp < 4 and cpi > 3:              # 低失業 + 高通膨 → 過熱
        return "過熱", "🟡", {"股": 50, "債": 50}
    if unemp > 5:                          # 高失業 → 復甦
        return "復甦", "🔵", {"股": 60, "債": 40}
    return "擴張", "🟢", {"股": 70, "債": 30}  # 其餘 → 擴張


def _fallback() -> dict:
    from datetime import datetime
    return {
        "phase": "未知",
        "emoji": "⚪",
        "allocation": {"股": 50, "債": 50},
        "indicators": {},
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
