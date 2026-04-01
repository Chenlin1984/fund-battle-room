"""
基金戰情室 — 主入口
目標環境：GitHub + Streamlit Cloud
"""
import streamlit as st
from utils.fetcher import get_fund_nav, search_fund
from utils.macro import get_macro_phase
from utils.portfolio import score_portfolio

st.set_page_config(page_title="基金戰情室", page_icon="📊", layout="wide")

# ── 側邊欄：4 大主題組合快選 ──────────────────────────────────────────
THEMES = {
    "🚀 全球科技爆發": ["安聯AI人工智慧", "貝萊德世界科技", "摩根美國科技"],
    "🇹🇼 台股強勢黑馬": ["野村優質", "統一黑馬", "安聯台灣科技"],
    "🏦 穩健配息平衡": ["安聯收益成長", "聯博全球高收益債"],
    "🛡️ 衰退避險防禦": ["富達美元債券", "摩根環球政府債"],
}

with st.sidebar:
    st.header("主題組合")
    theme = st.selectbox("選擇組合", list(THEMES.keys()))
    keywords = THEMES[theme]
    if st.button("🔄 強制刷新數據"):
        st.cache_data.clear()
        st.rerun()

# ── Tab 佈局 ──────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📡 總經面板", "🔍 基金診斷", "📂 投資組合"])

with tab1:
    st.subheader("總經資產配置燈號")
    # TODO: 呼叫 get_macro_phase() 並顯示景氣象限與建議配比
    st.info("總經面板開發中…")

with tab2:
    st.subheader("基金深度診斷")
    keyword = st.text_input("基金名稱關鍵字", placeholder="例：安聯AI")
    if keyword:
        # TODO: 呼叫 search_fund(keyword) 與 get_fund_nav(code)
        st.info("基金診斷功能開發中…")

with tab3:
    st.subheader(f"主題組合：{theme}")
    # TODO: 呼叫 score_portfolio(keywords)
    for kw in keywords:
        st.write(f"• {kw}")
