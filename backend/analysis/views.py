from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.data_loader import load_reviews, load_returns, load_sales, load_metadata
from .services.text_analysis import analyze_reviews_sentiment, extract_top_keywords
from .services.return_analysis import analyze_returns_summary
from .services.sales_analysis import analyze_sales_summary
from .services.aggregator import build_product_insights


def normalize_metadata(metadata):
    if isinstance(metadata, dict):
        return metadata

    # If metadata is a list of objects
    if isinstance(metadata, list):
        normalized = {}
        for item in metadata:
            asin = item.get("asin")
            if asin:
                normalized[asin] = item
        return normalized

    return {}


@api_view(["GET"])
def analyze_all(request):
    reviews_df = load_reviews()
    returns_df = load_returns()
    sales_df = load_sales()
    metadata_raw = load_metadata()
    metadata = normalize_metadata(metadata_raw)

    # Run analyses part
    reviews_summary = analyze_reviews_sentiment(reviews_df)
    return_reasons_map, return_counts = analyze_returns_summary(returns_df)
    sales_summary = analyze_sales_summary(sales_df)

    # Build final output part
    insights = build_product_insights(
        reviews_summary, return_reasons_map, return_counts, sales_summary, metadata
    )

    return Response(insights)


@api_view(["GET"])
def analyze_product(request, asin):
    reviews_df = load_reviews()
    returns_df = load_returns()
    sales_df = load_sales()
    metadata_raw = load_metadata()
    metadata = normalize_metadata(metadata_raw)

    reviews_summary = analyze_reviews_sentiment(reviews_df)
    return_reasons_map, return_counts = analyze_returns_summary(returns_df)
    sales_summary = analyze_sales_summary(sales_df)

    insights = build_product_insights(
        reviews_summary, return_reasons_map, return_counts, sales_summary, metadata
    )

    # Return only this product with asin id
    for item in insights:
        if str(item.get("asin")).lower() == str(asin).lower():
            return Response(item)

    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
