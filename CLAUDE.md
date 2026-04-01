# 核心開發與治理協議 (Core Protocol)

## §1 狀態與記憶管理 (State & Memory) [防斷線與省 Token 核心]
- **冷熱資料分離 (Hot/Cold Data)**：
  - **熱資料 (`STATE.md`)**：專案根目錄必須維持一個極簡的 `STATE.md`，包含核心檔案簡介、當前進度與待修復 Bug。每次新對話**僅限讀取此檔**掌握全局。
  - **冷資料 (Hooks 備份)**：系統已配置自動化 Hooks。Hook 1 將對話寫入 JSONL；Hook 2 備份計畫(Plan)版本。
- **冷資料檢索嚴格規範**：**絕對禁止**毫無理由地讀取完整的 JSONL 檔。僅在「撰寫 PR」、「生成報告」或「追溯 Bug」時，允許使用 `grep` 或 `tail` 精準抽樣。
- **隨手存檔 (Checkpointing)**：完成一個段落或發起 PR 前，必須主動更新 `STATE.md`，確保對話無縫接軌。

## §2 鋼鐵自省 (Ironclad Self-Audit)
在正式修改代碼或發起 PR 前，必須在對話框輸出簡短報告：
- [邏輯]：確保代碼 100% 符合需求。
- [邊界]：測試空值、極值、異常（如 Proxy Timeout）等極端場景。
- [效能]：確認是否已妥善運用 `st.cache_data` 避免重複運算，或適時使用 `st.cache_data.clear()` 同步數據。
- [Debug]：記錄已修正的潛在 Bug。

## §3 交付與部署掌控 (Delivery & Deployment)
- **環境鎖定**：目標環境為 GitHub Repo 聯動 Streamlit Cloud。所有代碼必須為 `.py` 腳本（絕對禁止 `.ipynb`）。必須維護精準的 `requirements.txt`。
- **PR 規範**：修改後必須使用 `gh pr create` 建立請求，並提供一鍵 Merge 指令 `gh pr merge <PR號碼> --merge --delete-branch` 供使用者操作。嚴禁 AI 自動 Merge。

## §4 節能與高效率 (Usage Efficiency)
- **閉嘴寫扣 (No-Yapping)**：跳過客套話與原理解釋，直接輸出代碼。
- **分步與局部編輯**：超過 50 行的修改需先用 3 句話確認藍圖。嚴禁整檔讀取與整檔覆蓋，針對特定函數局部替換。

## §5 卡關救援 (Anti-Loop Protocol)
- 針對同一個報錯，若連續重試 2 次未果，**嚴禁繼續盲目猜測**。
- 立即停機並輸出「外部 AI 諮詢清單」（精煉列出問題核心、終端機錯誤 Log 與相關代碼片段），交由使用者詢問其他 AI 進行雙重驗證。
