"""
數據爬蟲模組
- MoneyDJ 基金數據：走 Proxy
- FundClear 基金數據：走 Proxy
- FRED / yfinance 總經數據：直連
"""
import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# ── Proxy 設定（MoneyDJ / FundClear 使用）────────────────────────────
_PROXY_USER = os.environ.get("PROXY_USER", "")
_PROXY_PASS = os.environ.get("PROXY_PASS", "")
_PROXY_HOST = "chen10021.synology.me:3128"
PROXIES = {
    "http": f"http://{_PROXY_USER}:{_PROXY_PASS}@{_PROXY_HOST}",
    "https": f"http://{_PROXY_USER}:{_PROXY_PASS}@{_PROXY_HOST}",
} if _PROXY_USER else {}

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9",
}

MONEYDJ_BASE = "https://www.moneydj.com/funddj"


def _get(url: str, use_proxy: bool = False, **kwargs) -> requests.Response:
    """統一請求入口，含 Proxy 分流與超時設定。"""
    proxies = PROXIES if use_proxy else {}
    resp = requests.get(url, headers=_HEADERS, proxies=proxies, timeout=15, **kwargs)
    resp.raise_for_status()
    return resp


def search_fund(keyword: str) -> list[dict]:
    """
    FundClear 基金搜尋。
    回傳 [{"code": ..., "name": ...}, ...]
    """
    url = "https://www.fundclear.com.tw/investBase/goGetSearchFundList.action"
    params = {"keyword": keyword, "fundType": "2"}
    try:
        resp = _get(url, use_proxy=True, params=params)
        data = resp.json()
        return [{"code": f["fundCode"], "name": f["fundName"]} for f in data.get("list", [])]
    except Exception:
        return []


def get_fund_nav(fund_code: str, days: int = 90) -> pd.DataFrame:
    """
    FundClear 淨值 API。
    回傳 DataFrame[date, nav]；若數據異常（單日 ±15%）則停止渲染前先過濾。
    """
    end = datetime.today().strftime("%Y/%m/%d")
    start = (datetime.today() - timedelta(days=days)).strftime("%Y/%m/%d")
    url = (
        f"https://www.fundclear.com.tw/SmartFundAPI/api/FundAjax/GetFundNAV"
        f"?FundCode={fund_code}&StartDate={start}&EndDate={end}"
    )
    try:
        resp = _get(url, use_proxy=True)
        rows = resp.json().get("Data", [])
        df = pd.DataFrame(rows, columns=["date", "nav"])
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"])
        df = df.dropna().sort_values("date").reset_index(drop=True)
        # 防呆：單日漲跌 > ±15% 標記異常
        if len(df) > 1:
            pct = df["nav"].pct_change().abs()
            if pct.max() > 0.15:
                df["anomaly"] = pct > 0.15
        return df
    except Exception:
        return pd.DataFrame(columns=["date", "nav"])


def get_fred(series_id: str, api_key: str, limit: int = 60) -> pd.Series:
    """
    FRED 直連（不走 Proxy）。
    回傳 pd.Series，index 為日期。
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "limit": limit,
        "sort_order": "desc",
    }
    try:
        resp = _get(url, use_proxy=False, params=params)
        obs = resp.json().get("observations", [])
        s = pd.Series(
            {o["date"]: float(o["value"]) for o in obs if o["value"] != "."}
        )
        return s.sort_index()
    except Exception:
        return pd.Series(dtype=float)
