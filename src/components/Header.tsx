import { Home, Search, X, MessageCircle } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { chatBotRef } from "./ChatBot";

const Header = () => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const getLinkClasses = (path: string) => {
    const baseClasses = "text-sm font-medium transition-all duration-200 relative pb-2";
    if (isActive(path)) {
      return `${baseClasses} text-primary border-b-2 border-primary`;
    }
    return `${baseClasses} text-foreground hover:text-primary`;
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <Home className="h-8 w-8 text-primary" />
          <span className="text-xl font-bold text-foreground">Cedric House Planning</span>
        </Link>
        
        <nav className="hidden md:flex items-center gap-8">
          <Link to="/" className={getLinkClasses("/")}>
            Home
          </Link>
          <Link to="/house-plans" className={getLinkClasses("/house-plans")}>
            House Plans
          </Link>
          <Link to="/built-homes" className={getLinkClasses("/built-homes")}>
            Built Homes
          </Link>
          <Link to="/services" className={getLinkClasses("/services")}>
            Services
          </Link>
          <Link to="/about" className={getLinkClasses("/about")}>
            About
          </Link>
          <Link to="/contact" className={getLinkClasses("/contact")}>
            Contact
          </Link>
        </nav>
        
        <div className="flex items-center gap-4">
          <Button 
            onClick={() => chatBotRef.current?.open()}
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold shadow-lg hover:shadow-xl transition-all hover:scale-105 flex items-center gap-2"
          >
            <MessageCircle className="w-4 h-4" />
            Munyai AI
          </Button>
          <Link to="/get-quote">
            <Button className="bg-orange-500 hover:bg-orange-600 text-white font-bold shadow-lg hover:shadow-xl transition-all hover:scale-105">
              Get FREE Quote Now
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
