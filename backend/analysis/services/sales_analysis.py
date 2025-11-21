import pandas as pd

def analyze_sales_summary(sales_df: pd.DataFrame):
    """
    Returns: { asin: { total_units_sold, total_gmv, total_refunds, weekly: [{week, units_sold, gmv}], ... } }
    """
    if sales_df is None or sales_df.empty:
        return {}

    df = sales_df.copy()
    if "asin" not in df.columns:
        raise ValueError("sales CSV must have 'asin' column")

    result = {}
    for asin, grp in df.groupby("asin"):
        total_units = int(grp["units_sold"].sum())
        total_gmv = float(grp["gmv"].sum())
        total_refunds = int(grp["refunds"].sum()) if "refunds" in grp.columns else 0
        weekly = grp.sort_values("week").to_dict(orient="records")
        result[str(asin)] = {
            "total_units_sold": total_units,
            "total_gmv": total_gmv,
            "total_refunds": total_refunds,
            "weekly": weekly
        }
    return result
