import { useEffect, useState } from "react";
import { fetchProducts } from "../services/api";
import Loader from "../components/Loader";
import { Link } from "react-router-dom";

export default function Issues() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts().then((res) => {
      setProducts(res);
      setLoading(false);
    });
  }, []);

  if (loading) return <Loader />;

  const productsWithIssues = products.filter((p) => p.top_issues.length > 0);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Product Issues</h1>

      <div className="space-y-4">
        {productsWithIssues.map((p) => (
          <div key={p.asin} className="p-4 bg-white shadow rounded-lg">
            <h2 className="text-xl font-semibold">{p.product_name}</h2>
            <p className="text-gray-700">ASIN: {p.asin}</p>

            <ul className="list-disc ml-6 mt-2 text-red-600">
              {p.top_issues.map((issue: string, i: number) => (
                <li key={i}>{issue}</li>
              ))}
            </ul>

            <Link
              to={`/product/${p.asin}`}
              className="text-blue-500 underline mt-2 inline-block"
            >
              View Details
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
