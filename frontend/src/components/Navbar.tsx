import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, Flag } from "lucide-react";

export default function Navbar() {
  const { pathname } = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/", icon: <LayoutDashboard size={18} /> },
    { name: "Issues", path: "/issues", icon: <Flag size={18} /> },
  ];

  return (
    <nav className="backdrop-blur-xl bg-gray-900/80 shadow-2xl sticky top-0 z-50 border-b border-gray-800/50">
      <div className="container mx-auto flex items-center justify-between py-4 px-4">

        {/* Logo */}
        <div className="text-3xl font-bold tracking-wider flex items-center gap-1 select-none">
          <span className="text-blue-400">Merch</span>
          <span className="text-white">Tech</span>
        </div>

        {/* Menu */}
        <div className="hidden md:flex items-center space-x-6">
          {menuItems.map((item) => {
            const isActive = pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`relative px-5 py-2 rounded-xl font-medium text-lg flex items-center gap-2
                  transition-all duration-300
                  ${
                    isActive
                      ? "text-white bg-gradient-to-r from-blue-600/40 to-blue-400/30 shadow-lg shadow-blue-500/20 scale-105"
                      : "text-gray-300 hover:text-white hover:bg-gray-700/40 hover:shadow-md"
                  }
                `}
              >
                {/* Icon */}
                <span className="opacity-80">{item.icon}</span>

                {/* Text */}
                {item.name}

                {/* Animated underline */}
                <span
                  className={`absolute left-0 bottom-[-4px] h-[3px] rounded-full bg-blue-400 transition-all duration-300 ${
                    isActive ? "w-full" : "w-0 group-hover:w-full"
                  }`}
                ></span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
