import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings

from analysis.services.data_loader import load_reviews, load_returns, load_sales, load_metadata
from analysis.services.text_analysis import analyze_reviews_sentiment, extract_top_keywords
from analysis.services.return_analysis import analyze_returns_summary
from analysis.services.sales_analysis import analyze_sales_summary
from analysis.services.aggregator import build_product_insights


class Command(BaseCommand):
    help = "Generate product insights automatically and save to JSON"

    def handle(self, *args, **kwargs):
        try:
            # Load datasets
            reviews_df = load_reviews()
            returns_df = load_returns()
            sales_df = load_sales()
            metadata = load_metadata()

            # Analyze datasets
            reviews_summary = analyze_reviews_sentiment(reviews_df)
            return_reasons_map, return_counts = analyze_returns_summary(returns_df)
            sales_summary = analyze_sales_summary(sales_df)

            # Generate insights
            insights = build_product_insights(
                reviews_summary, return_reasons_map, return_counts, sales_summary, metadata
            )

            # Save insights to JSON file
            output_path = os.path.join(getattr(settings, "DATA_DIR"), "insights_auto.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(insights, f, indent=2)

            self.stdout.write(self.style.SUCCESS(f"Insights generated and saved to {output_path}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error generating insights: {e}"))
