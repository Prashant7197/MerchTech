from textblob import TextBlob
import re
from collections import Counter
import pandas as pd

def _clean_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def analyze_reviews_sentiment(reviews_df: pd.DataFrame):
    """
    Returns dict:
      { asin: { avg_rating, total_reviews, avg_sentiment, negative_reviews: [texts] } }
    """
    if reviews_df is None or reviews_df.empty:
        return {}

    df = reviews_df.copy()
    # ensure expected columns exist
    if "asin" not in df.columns:
        raise ValueError("reviews must have 'asin' column")
    if "review_text" not in df.columns and "review" in df.columns:
        df["review_text"] = df["review"]
    if "rating" not in df.columns:
        df["rating"] = None

    df["clean_text"] = df["review_text"].apply(_clean_text)
    df["sentiment"] = df["clean_text"].apply(lambda t: TextBlob(t).sentiment.polarity if t else 0.0)
    result = {}
    for asin, grp in df.groupby("asin"):
        avg_rating = float(grp["rating"].dropna().mean()) if grp["rating"].notna().any() else None
        avg_sent = float(grp["sentiment"].mean())
        neg_texts = grp[grp["sentiment"] < 0]["review_text"].astype(str).tolist()
        result[str(asin)] = {
            "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
            "total_reviews": int(len(grp)),
            "avg_sentiment": round(avg_sent, 3),
            "negative_reviews": neg_texts,
            # top keywords (simple)
            "top_keywords": [k for k,_ in Counter(" ".join(grp["clean_text"]).split()).most_common(8) if len(k) > 3]
        }
    return result

def extract_top_keywords(texts, top_n=8):
    words = []
    for t in texts:
        words += _clean_text(t).split()
    freq = Counter([w for w in words if len(w) > 3])
    return [w for w,_ in freq.most_common(top_n)]
