import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Issues from "./pages/Issues";
import ProductDetails from "./pages/ProductDetails";
import NotFound from "./pages/NotFound";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <BrowserRouter>
        <Navbar />

        {/* Page wrapper */}
        <div className="container mx-auto px-4 py-6">
          <div className="bg-gray-800/40 backdrop-blur-md rounded-2xl shadow-2xl p-6 border border-gray-700/50">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/issues" element={<Issues />} />
              <Route path="/product/:id" element={<ProductDetails />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </div>
  );
}
