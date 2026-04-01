# STATE.md — 基金戰情室 狀態追蹤

_最後更新：2026-04-01_

## 部署資訊
| 項目 | 網址 |
|------|------|
| GitHub Repo | https://github.com/Chenlin1984/fund-battle-room (Public, branch: master) |
| Streamlit App | https://fund-battle-room-t8xcgqvn2bdgaygjaiodkk.streamlit.app |

## 核心檔案簡介

| 檔案 | 說明 | 狀態 |
|------|------|------|
| `CLAUDE.md` | 核心開發治理協議（5 大板塊） | ✅ 完成 |
| `app.py` | Streamlit 主入口，含 4 大主題快選側邊欄、3 個 Tab 骨架 | ⬜ 骨架，待填充 |
| `utils/fetcher.py` | 數據爬蟲：MoneyDJ/FundClear（Proxy）、FRED（直連），含防呆 ±15% 異常過濾 | ⬜ 骨架，待測試 |
| `utils/macro.py` | FRED 景氣象限判定（🟢擴張/🔵復甦/🟡過熱/🔴衰退），`st.cache_data` TTL=3600 | ⬜ 骨架，待測試 |
| `utils/portfolio.py` | 動能診斷（MA20/MA60 多頭排列）+ MDD 計算 + Sharpe | ⬜ 骨架，待測試 |
| `requirements.txt` | Streamlit Cloud 精準依賴（排除 Colab 專用套件） | ✅ 完成 |
| `.streamlit/config.toml` | 深色主題設定 | ✅ 完成 |

## 目前開發進度

**已完成：**
- ✅ CLAUDE.md 5 板塊協議
- ✅ 專案資料夾骨架（app.py / utils/ / requirements.txt / .gitignore）
- ✅ GitHub Repo 建立 + 首次 Push（2 commits）
- ✅ Streamlit Cloud 串接完成

**待開發（下一步）：**
- ⬜ `utils/macro.py` — FRED 真實數據串接與象限 UI 渲染
- ⬜ `utils/fetcher.py` — MoneyDJ / FundClear 爬蟲完整實作與 Proxy 驗證
- ⬜ `app.py` Tab1（總經面板）完整 UI
- ⬜ `app.py` Tab2（基金診斷）完整 UI
- ⬜ Streamlit Secrets 設定（PROXY_USER / PROXY_PASS / FRED_API_KEY）

## 待修復 Bug 清單

- （目前無）
