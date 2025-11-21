export interface Product {
  asin: string;
  product_name: string;
  category: string | null;
  metrics: {
    gmv: number;
    units_sold: number;
    refunds: number;
    avg_rating: number;
    total_reviews: number;
    avg_sentiment: number;
    return_rate: number;
  };
  top_return_reasons: Record<string, number>;
  top_review_keywords: string[];
  top_issues: string[];
  suggested_actions: string[];
  weekly_sales: any[];
}

const BASE_URL = "http://127.0.0.1:8000/api";

// Fetch ALL product insights
export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch(`${BASE_URL}/analyze/`);
  return res.json();
}

// Fetch SINGLE product by ASIN
export async function fetchProductById(asin: string): Promise<Product> {
  const res = await fetch(`${BASE_URL}/analyze/${asin}/`);
  return res.json();
}

export async function fetchAutoInsights() {
  const res = await fetch(`${BASE_URL}/auto-insights/`);
  return res.json();
}

