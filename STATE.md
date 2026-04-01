# STATE.md — 基金戰情室 狀態追蹤

_最後更新：2026-04-01_

## GitHub Repo
`https://github.com/Chenlin1984/fund-battle-room` (Public, branch: master)

## 核心檔案簡介

| 檔案 | 說明 |
|------|------|
| `CLAUDE.md` | 核心開發治理協議（5 大板塊） |
| `app.py` | Streamlit 主入口（骨架，待開發） |
| `utils/fetcher.py` | 數據爬蟲（MoneyDJ/FundClear/FRED，含 Proxy 設定，骨架） |
| `utils/macro.py` | 總經引擎（FRED 景氣象限判定，骨架） |
| `utils/portfolio.py` | 投資組合引擎（骨架） |
| `requirements.txt` | Streamlit Cloud 精準依賴清單 |

## 目前開發進度

- ✅ CLAUDE.md 協議寫入完成（5 板塊）
- ✅ 專案資料夾骨架建立完成
- ⬜ `app.py` 總經面板 UI — 待開發
- ⬜ `utils/fetcher.py` 基金數據爬蟲 — 待開發
- ⬜ `utils/macro.py` FRED 景氣象限邏輯 — 待開發
- ✅ GitHub Repo 初始化完成：https://github.com/Chenlin1984/fund-battle-room
- ✅ Streamlit Cloud 部署完成：https://fund-battle-room-t8xcgqvn2bdgaygjaiodkk.streamlit.app

## 待修復 Bug 清單

- （目前無）
