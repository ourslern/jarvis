import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Sidebar } from "./components/layout/Sidebar";
import { Dashboard } from "./pages/Dashboard";
import { Models } from "./pages/Models";
import { Containers } from "./pages/Containers";
import { Performance } from "./pages/Performance";
import { Chat } from "./pages/Chat";
import { Settings } from "./pages/Settings";
import "./App.css";

export default function App() {
  return (
    <BrowserRouter>
      <div className="shell">
        <Sidebar />
        <main className="main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/models" element={<Models />} />
            <Route path="/containers" element={<Containers />} />
            <Route path="/performance" element={<Performance />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
