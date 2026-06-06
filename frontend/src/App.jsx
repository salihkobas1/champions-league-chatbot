import { useState } from "react";
import { sendChatMessage } from "./api/chatApi";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! Ask me a Champions League history question.",
      route: null,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend(e) {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage = input.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userMessage, route: null },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(userMessage);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.answer,
          route: data.route,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Sorry, something went wrong while contacting the backend.",
          route: "error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <h1>Champions League Chatbot</h1>
          <p>Ask historical UEFA Champions League questions</p>
        </header>

        <main className="chat-window">
          {messages.map((message, index) => (
            <div key={index} className={`message-row ${message.role}`}>
              <div className={`message-bubble ${message.role}`}>
                <p>{message.text}</p>

                {message.route && (
                  <span className={`route-badge ${message.route}`}>
                    {message.route.toUpperCase()}
                  </span>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row bot">
              <div className="message-bubble bot">
                <p>Thinking...</p>
              </div>
            </div>
          )}
        </main>

        <form className="chat-input-area" onSubmit={handleSend}>
          <input
            type="text"
            placeholder="Ask something like: Who is the 5th highest goalscorer?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;