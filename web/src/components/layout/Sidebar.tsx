import { NavLink } from "react-router-dom";
import { Home, Bot, Boxes, MessageSquare, LineChart, Settings } from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: <Home /> },
  { to: "/models", label: "Models", icon: <Bot /> },
  { to: "/containers", label: "Containers", icon: <Boxes /> },
  { to: "/performance", label: "Performance", icon: <LineChart /> },
  { to: "/chat", label: "Chat", icon: <MessageSquare /> },
  { to: "/settings", label: "Settings", icon: <Settings /> },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">JARVIS</div>
      <div className="tag">Local AI OS</div>

      <nav>
        {links.map((link) => (
          <NavLink key={link.to} to={link.to} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            {link.icon}
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
