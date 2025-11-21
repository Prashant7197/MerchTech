import pandas as pd
from collections import defaultdict

def analyze_returns_summary(returns_df: pd.DataFrame):
    """
    returns:
      return_reasons_map: { asin: { reason: count, ... }, ... }
      return_counts: { asin: total_count, ... }
    """
    if returns_df is None or returns_df.empty:
        return {}, {}
    df = returns_df.copy()
    # normalize column names: expect asin, return_reason, count
    if "asin" not in df.columns:
        raise ValueError("returns CSV must have 'asin' column")
    # some returns csv may have repeated rows - aggregate
    grouped = df.groupby(["asin", "return_reason"])["count"].sum().reset_index()
    reasons = defaultdict(dict)
    counts = {}
    for asin, g in grouped.groupby("asin"):
        r = {row["return_reason"]: int(row["count"]) for _, row in g.iterrows()}
        reasons[str(asin)] = r
        counts[str(asin)] = int(g["count"].sum())
    return reasons, counts
