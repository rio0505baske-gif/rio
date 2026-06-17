"use client";
import { useState, useRef, useEffect } from "react";

const SUGGESTIONS = {
  all: ["A3フルカラー500部の概算は？","入稿データの解像度規定を教えて","名刺の標準制作フローは？","塗り足しって何mm必要？"],
  estimate: ["A4両面500部の概算は？","A3フルカラー500部の概算は？","PP加工するといくら上がる？","名刺両面1000枚の概算は？"],
  spec: ["塗り足しって何mm必要？","解像度規定を教えて","カラーモードはCMYK？","フォントのアウトライン化とは？"],
  flow: ["名刺の標準制作フローは？","チラシのリードタイムは？","急ぎで対応できる？","入稿前チェックリストを教えて"],
};

type Tab = keyof typeof SUGGESTIONS;

export default function Home() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "こんにちは！印刷・広告会社の社内AIアシスタントです。\n見積もり・入稿規定・制作進行について何でも聞いてください。" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState<Tab>("all");
  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => { bottom.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

  const send = async (text?: string) => {
    const t = (text || input).trim();
    if (!t || loading) return;
    setInput("");
    const next = [...messages, { role: "user", content: t }];
    setMessages(next);
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: next.map(m => ({ role: m.role, content: m.content })) }),
      });
      const data = await res.json();
      setMessages(p => [...p, { role: "assistant", content: data.content }]);
    } catch {
      setMessages(p => [...p, { role: "assistant", content: "エラーが発生しました。" }]);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: "all" as Tab, label: "すべて" },
    { id: "estimate" as Tab, label: "💰 見積もり" },
    { id: "spec" as Tab, label: "📋 入稿規定" },
    { id: "flow" as Tab, label: "📅 制作進行" },
  ];

  return (
    <div className="h-screen bg-[#1a1612] flex flex-col font-sans overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-[#2a2218] flex items-center gap-3 shrink-0">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[#c8a96e] to-[#8b6914] flex items-center justify-center text-lg shrink-0">🖨</div>
        <div>
          <div className="text-[#e8d9be] font-semibold text-base">Print & Ad Assistant</div>
          <div className="text-[#6a5a42] text-xs">社内AIアシスタント</div>
        </div>
        <div className="ml-auto flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-green-500"/>
          <span className="text-[#6a5a42] text-xs">稼働中</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-[#2a2218] shrink-0 overflow-x-auto">
        {tabs.map(({ id, label }) => (
          <button key={id} onClick={() => setTab(id)}
            className={`px-3 py-2 text-xs whitespace-nowrap border-b-2 transition-colors ${
              tab === id ? "border-[#c8a96e] text-[#c8a96e] font-bold" : "border-transparent text-[#4a3f30]"
            }`}>
            {label}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            {m.role === "assistant" && (
              <div className="w-6 h-6 rounded-md bg-gradient-to-br from-[#c8a96e] to-[#8b6914] flex items-center justify-center text-xs mr-2 shrink-0 mt-1">🖨</div>
            )}
            <div className={`max-w-[80%] px-3 py-2 text-sm leading-relaxed ${
              m.role === "user"
                ? "bg-gradient-to-br from-[#c8a96e] to-[#a07832] text-[#1a1612] rounded-[13px_3px_13px_13px]"
                : "bg-[#221e18] text-[#d0bfa0] border border-[#2a2218] rounded-[3px_13px_13px_13px]"
            }`}>
              {m.content.split("\n").map((l, j, a) => <span key={j}>{l}{j < a.length-1 && <br/>}</span>)}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-start gap-2">
            <div className="w-6 h-6 rounded-md bg-gradient-to-br from-[#c8a96e] to-[#8b6914] flex items-center justify-center text-xs shrink-0">🖨</div>
            <div className="px-3 py-2 bg-[#221e18] border border-[#2a2218] rounded-[3px_13px_13px_13px]">
              <div className="flex gap-1">
                {[0,1,2].map(i => <div key={i} className="w-2 h-2 rounded-full bg-[#c8a96e] animate-bounce" style={{animationDelay:`${i*0.15}s`}}/>)}
              </div>
            </div>
          </div>
        )}
        <div ref={bottom}/>
      </div>

      {/* Suggestions */}
      <div className="px-4 pb-2 shrink-0">
        <div className="text-[9px] text-[#3a3020] mb-1 uppercase tracking-widest">クイック質問</div>
        <div className="flex flex-wrap gap-1">
          {SUGGESTIONS[tab].map((s, i) => (
            <button key={i} onClick={() => send(s)}
              className="px-3 py-1 text-xs border border-[#2a2218] rounded-full text-[#6a5a42] hover:border-[#c8a96e] hover:text-[#c8a96e] transition-colors">
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="px-4 pb-5 pt-2 border-t border-[#2a2218] shrink-0">
        <div className="flex gap-2 items-end bg-[#221e18] border border-[#2e2820] rounded-xl px-3 py-2 focus-within:border-[#c8a96e] transition-colors">
          <textarea value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();} }}
            placeholder="質問を入力… (Enter送信)" rows={1}
            className="flex-1 bg-transparent border-none outline-none text-[#d0bfa0] text-sm leading-relaxed resize-none max-h-24 overflow-y-auto"/>
          <button onClick={() => send()} disabled={loading||!input.trim()}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-sm shrink-0 transition-all disabled:bg-[#2a2218] disabled:text-[#3a3020] bg-gradient-to-br from-[#c8a96e] to-[#8b6914] text-[#1a1612]">
            ↑
          </button>
        </div>
      </div>
    </div>
  );
}
