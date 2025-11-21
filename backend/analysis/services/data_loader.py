import os
import pandas as pd
import json
from django.conf import settings


def _path(filename):
    p = os.path.join(getattr(settings, "DATA_DIR"), filename)
    if not os.path.exists(p):
        raise FileNotFoundError(f"Dataset not found: {p}")
    return p


def load_reviews():
    return pd.read_csv(_path("sde2_reviews.csv"))


def load_returns():
    return pd.read_csv(_path("sde2_returns.csv"))


def load_sales():
    return pd.read_csv(_path("sde2_sales.csv"))


def _normalize_meta_value(val):
    if isinstance(val, dict):
        return val

    if isinstance(val, str):
        return {
            "product_name": val,
            "title": val
        }

    if isinstance(val, list):
        if len(val) == 0:
            return {}

        first = val[0]

        if isinstance(first, dict):
            return first
        else:
            return {
                "product_name": str(first),
                "title": str(first)
            }

    return {
        "product_name": str(val),
        "title": str(val)
    }


def load_metadata():
    json_path = os.path.join(getattr(settings, "DATA_DIR"), "sde2_merchtech_dataset.json")

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            j = json.load(f)

            clean_meta = {}

            # handle dict of JSON
            if isinstance(j, dict):
                for key, val in j.items():
                    key_lower = str(key).lower()
                    if key_lower in ["products", "generated_at", "version"]:
                        continue
                    clean_meta[str(key)] = val
                return clean_meta

            # handle list of JSON
            if isinstance(j, list):
                meta = {}
                for item in j:
                    asin = item.get("asin") or item.get("id") or None
                    if asin:
                        meta[str(asin)] = item
                return meta
            
    return {}

