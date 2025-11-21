from textblob import TextBlob
import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()

def analyze_reviews(df):
    df = df.copy()

    df["review_text"] = df["review_text"].apply(clean_text)
    df["sentiment"] = df["review_text"].apply(
        lambda t: TextBlob(t).sentiment.polarity if t else 0
    )
    df["is_negative"] = df["sentiment"] < 0

    return df
