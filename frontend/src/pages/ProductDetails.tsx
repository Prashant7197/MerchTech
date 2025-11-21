import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function ProductDetails() {
    const { id } = useParams();
    const [product, setProduct] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/analyze/${id}/`)
            .then((res) => res.json())
            .then((data) => {
                setProduct(data);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [id]);

    if (loading) return <p className="p-4">Loading...</p>;
    if (!product) return <p className="p-4 text-red-600">Product not found</p>;

    return (
        <div className="p-4 max-w-4xl mx-auto">
            
            {/* PRODUCT HEADER */}
            <h1 className="text-3xl font-bold mb-2">{product.product_name}</h1>
            <p className="text-gray-500 mb-6">ASIN: {product.asin}</p>

            {/* METRICS */}
            <h2 className="text-xl font-semibold mb-2">Product Metrics</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
                {product.metrics &&
                    Object.entries(product.metrics).map(([key, value]) => (
                        <div key={key} className="bg-white shadow p-4 rounded">
                            <p className="text-sm text-gray-500 capitalize">
                                {key.replace(/_/g, " ")}
                            </p>
                            <p className="text-xl font-semibold">{value}</p>
                        </div>
                    ))}
            </div>

            {/* TOP ISSUES */}
            <div className="bg-red-50 border border-red-200 p-4 rounded mb-6">
                <h2 className="text-xl font-bold mb-2 text-red-700">Top Issues</h2>
                {product.top_issues?.length ? (
                    <ul className="list-disc ml-6">
                        {product.top_issues.map((issue: string, index: number) => (
                            <li key={index} className="text-red-700">{issue}</li>
                        ))}
                    </ul>
                ) : (
                    <p className="text-gray-600">No major issues detected.</p>
                )}
            </div>

            {/* SUGGESTED ACTIONS */}
            <div className="bg-blue-50 border border-blue-200 p-4 rounded mb-6">
                <h2 className="text-xl font-bold mb-2 text-blue-700">Suggested Actions</h2>
                {product.suggested_actions?.length ? (
                    <ul className="list-disc ml-6">
                        {product.suggested_actions.map((action: string, index: number) => (
                            <li key={index} className="text-blue-700">{action}</li>
                        ))}
                    </ul>
                ) : (
                    <p className="text-gray-600">No suggested actions available.</p>
                )}
            </div>

            {/* RETURN REASONS */}
            <div className="bg-white shadow p-4 rounded mb-6">
                <h2 className="text-xl font-bold mb-3">Top Return Reasons</h2>
                {product.top_return_reasons &&
                Object.keys(product.top_return_reasons).length > 0 ? (
                    <ul className="list-disc ml-6">
                        {Object.entries(product.top_return_reasons).map(
                            ([reason, count]) => (
                                <li key={reason}>
                                    {reason} — <b>{count}</b>
                                </li>
                            )
                        )}
                    </ul>
                ) : (
                    <p className="text-gray-500">No return data.</p>
                )}
            </div>

            {/* REVIEW KEYWORDS
            <div className="bg-white shadow p-4 rounded mb-6">
                <h2 className="text-xl font-bold mb-3">Top Review Keywords</h2>
                {product.top_review_keywords?.length ? (
                    <ul className="space-y-2">
                        {product.top_review_keywords.map(
                            (kw: string, index: number) => (
                                <li
                                    key={index}
                                    className="p-2 bg-gray-100 rounded border border-gray-300 text-gray-800"
                                >
                                    {kw}
                                </li>
                            )
                        )}
                    </ul>
                ) : (
                    <p className="text-gray-500">No keywords extracted.</p>
                )}
            </div> */}

            {/* WEEKLY SALES SECTION */}
            <div className="bg-white shadow p-5 rounded-xl mb-8">
                <h2 className="text-xl font-bold mb-4">Weekly Sales Summary</h2>

                {product.weekly_sales?.length ? (
                    <div className="overflow-x-auto">
                        <table className="min-w-full border border-gray-200 rounded-lg overflow-hidden">
                            <thead>
                                <tr className="bg-gray-100 text-gray-700 text-sm uppercase tracking-wide">
                                    <th className="p-3 border-b">Week</th>
                                    <th className="p-3 border-b">Units Sold</th>
                                    <th className="p-3 border-b">GMV ($)</th>
                                    <th className="p-3 border-b">Refunds</th>
                                </tr>
                            </thead>

                            <tbody>
                                {product.weekly_sales.map((ws: any, index: number) => (
                                    <tr
                                        key={index}
                                        className={`text-center text-gray-800 ${
                                            index % 2 === 0 ? "bg-gray-50" : "bg-white"
                                        } hover:bg-blue-50 transition`}
                                    >
                                        <td className="p-3 border-b font-medium">{ws.week}</td>
                                        <td className="p-3 border-b">{ws.units_sold}</td>
                                        <td className="p-3 border-b">{ws.gmv}</td>
                                        <td className="p-3 border-b">{ws.refunds}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p className="text-gray-500">No weekly sales data.</p>
                )}
            </div>

        </div>
    );
}
