import { useState } from "react";
import { askJarvis } from "../api/jarvis";
import { Card } from "../components/Card";
import { Header } from "../components/layout/Header";

export function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState<string[]>([]);

  async function send() {
    if (!message.trim()) return;
    const msg = message.trim();
    setChat((c) => [...c, `You: ${msg}`]);
    setMessage("");

    const res = await askJarvis(msg);
    setChat((c) => [...c, `Jarvis: ${res.response || JSON.stringify(res)}`]);
  }

  return (
    <>
      <Header title="Chat" subtitle="Talk directly to Jarvis" />
      <Card title="Conversation" className="chat-card">
        <div className="chat-log">
          {chat.map((line, i) => <div key={i}>{line}</div>)}
        </div>
        <div className="chat-input">
          <input value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => e.key === "Enter" && send()} placeholder="Ask Jarvis..." />
          <button onClick={send}>Send</button>
        </div>
      </Card>
    </>
  );
}
