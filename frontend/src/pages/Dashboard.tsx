import { useEffect, useState } from "react";
import { fetchAutoInsights } from "../services/api";
import Loader from "../components/Loader";

export default function Dashboard() {
  const [insights, setInsights] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAutoInsights().then((res) => {
      setInsights(res);
      setLoading(false);
    });
  }, []);

  if (loading) return <Loader />;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Automated Product Insights</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-white shadow rounded-lg">
          <h2 className="text-xl font-semibold">Total Products</h2>
          <p className="text-2xl font-bold text-blue-600">{insights.length}</p>
        </div>
        <div className="p-4 bg-white shadow rounded-lg">
          <h2 className="text-xl font-semibold">Total Issues</h2>
          <p className="text-2xl font-bold text-red-600">
            {insights.reduce((sum, p) => sum + p.top_issues.length, 0)}
          </p>
        </div>
        <div className="p-4 bg-white shadow rounded-lg">
          <h2 className="text-xl font-semibold">Updated From Automation</h2>
          <p className="text-lg text-green-600">✔ Auto-Generated</p>
        </div>
      </div>

      <h2 className="text-2xl font-bold mb-2">Products Overview</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {insights.map((item) => (
          <div key={item.asin} className="p-4 bg-gray-50 shadow rounded-lg">
            <h3 className="text-xl font-semibold">{item.product_name}</h3>
            <p className="text-gray-600">ASIN: {item.asin}</p>

            <p className="mt-2">
              <strong>Issues: </strong>{item.top_issues.length}
            </p>

            <a
              href={`/product/${item.asin}`}
              className="mt-3 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              View Details
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
