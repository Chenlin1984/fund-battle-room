"""
投資組合引擎 — 基金動能與 MDD 診斷
"""
import numpy as np
import pandas as pd
import streamlit as st
from utils.fetcher import get_fund_nav, search_fund


@st.cache_data(ttl=1800)
def score_portfolio(keywords: list[str]) -> list[dict]:
    """
    對一組關鍵字搜尋基金並計算動能與 MDD。
    回傳 [{"name", "code", "signal", "mdd", "ma_ok"}, ...]
    """
    results = []
    for kw in keywords:
        funds = search_fund(kw)
        if not funds:
            results.append({"name": kw, "code": None, "signal": "⚠️ 找不到", "mdd": None, "ma_ok": None})
            continue
        f = funds[0]
        df = get_fund_nav(f["code"], days=365)
        if df.empty:
            results.append({"name": f["name"], "code": f["code"], "signal": "⚠️ 無法取得淨值", "mdd": None, "ma_ok": None})
            continue

        nav = df["nav"]
        ma20 = nav.rolling(20).mean().iloc[-1]
        ma60 = nav.rolling(60).mean().iloc[-1]
        latest = nav.iloc[-1]
        ma_ok = latest > ma20 > ma60

        # 最大回撤
        roll_max = nav.cummax()
        drawdown = (nav - roll_max) / roll_max
        mdd = round(float(drawdown.min()) * 100, 1)

        signal = "🟢 趨勢向上(建議扣款)" if ma_ok else "🔴 弱勢觀望"
        if mdd < -15:
            signal += " ⚠️ 波動風險過高"

        results.append({
            "name": f["name"],
            "code": f["code"],
            "signal": signal,
            "mdd": mdd,
            "ma_ok": ma_ok,
        })
    return results


def calc_sharpe(nav_series: pd.Series, risk_free: float = 0.02) -> float:
    """年化夏普值。"""
    returns = nav_series.pct_change().dropna()
    if returns.std() == 0:
        return 0.0
    ann_return = returns.mean() * 252
    ann_vol = returns.std() * np.sqrt(252)
    return round((ann_return - risk_free) / ann_vol, 2)
