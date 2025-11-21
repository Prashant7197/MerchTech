import numpy as np
from collections import defaultdict

# Normalizes metadata for a single ASIN. Ensures meta is always a DICTIONARY.
def normalize_metadata(meta):
    if isinstance(meta, dict):
        return meta

    if isinstance(meta, str):
        return {
            "product_name": meta,
            "title": meta
        }

    if isinstance(meta, list):
        # pick first dict entry if list of dicts
        if len(meta) > 0:
            if isinstance(meta[0], dict):
                return meta[0]
            else:
                # list of strings / numbers
                return {
                    "product_name": str(meta[0]),
                    "title": str(meta[0])
                }
        return {}

    # anything else fallback
    return {}


def build_product_insights(
    reviews_summary,
    return_reasons_map,
    return_counts,
    sales_summary,
    metadata
):
    """
    Build unified insights for all products
    """
    insights = []

    # median GMV to detect low performers
    gmv_values = [v.get("total_gmv", 0) for v in sales_summary.values()]
    median_gmv = sorted(gmv_values)[len(gmv_values)//2] if gmv_values else 0

    # unified ASIN list from all sources
    asins = set(list(sales_summary.keys()) +
                list(metadata.keys()) +
                list(reviews_summary.keys()))

    for asin in sorted(asins):
        raw_meta = metadata.get(str(asin), {}) if isinstance(metadata, dict) else {}
        meta = normalize_metadata(raw_meta)

        sales = sales_summary.get(str(asin), {})
        reviews = reviews_summary.get(str(asin), {})
        reasons = return_reasons_map.get(str(asin), {})

        total_returns = return_counts.get(str(asin), 0)
        units = sales.get("total_units_sold", 0)
        gmv = sales.get("total_gmv", 0)
        refunds = sales.get("total_refunds", 0)

        avg_rating = reviews.get("avg_rating", None)
        avg_sentiment = reviews.get("avg_sentiment", 0)
        total_reviews = reviews.get("total_reviews", 0)
        keywords = reviews.get("top_keywords", [])

        # Return rate
        return_rate = (total_returns / units) if units > 0 else 0.0

        issues = []
        actions = []

        if gmv < median_gmv:
            issues.append("Low GMV vs peer median")
            actions.append("Investigate visibility, repricing, or marketing for this product")

        if return_rate > 0.15:
            issues.append("High return rate")
            actions.append("Analyze top return reasons to improve quality, sizing or packaging")

        if avg_rating is not None and avg_rating < 3.0:
            issues.append("Low average rating (< 3.0)")
            actions.append("Improve listing quality, description accuracy, and images")

        if avg_sentiment < 0:
            issues.append("Negative review sentiment")
            actions.append("Fix product quality or mismatched descriptions")

        # Return reason-based tailored actions
        for reason, cnt in reasons.items():
            reason_l = reason.lower()
            if "size" in reason_l:
                actions.append("Improve sizing chart and provide fit photos")
            if "defect" in reason_l or "damag" in reason_l:
                actions.append("Enhance QC and packaging process")
            if "late" in reason_l or "delivery" in reason_l:
                actions.append("Improve shipping SLA accuracy and courier performance")

        # Deduplicate actions
        deduped_actions = []
        for a in actions:
            if a not in deduped_actions:
                deduped_actions.append(a)

        insight = {
            "asin": asin,
            "product_name": meta.get("product_name") or meta.get("title") or f"ASIN {asin}",
            "category": meta.get("category", None),

            "metrics": {
                "gmv": gmv,
                "units_sold": units,
                "refunds": refunds,
                "avg_rating": avg_rating,
                "total_reviews": total_reviews,
                "avg_sentiment": avg_sentiment,
                "return_rate": round(return_rate, 3),
            },

            "top_return_reasons": reasons,
            "top_review_keywords": keywords,
            "top_issues": issues,
            "suggested_actions": deduped_actions,
            "weekly_sales": sales.get("weekly", []),
        }

        insights.append(insight)

    insights.sort(key=lambda x: (-len(x["top_issues"]), x["metrics"]["gmv"]))

    return insights
