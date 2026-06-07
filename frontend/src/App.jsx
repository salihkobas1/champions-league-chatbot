import { useEffect, useRef, useState } from "react";
import { sendChatMessage, getChatHistory, clearChatHistory } from "./api/chatApi";
import { loginUser, registerUser, getMe } from "./api/authApi";
import "./App.css";

const INITIAL_MESSAGES = [
  {
    role: "bot",
    text: "Hi! Ask me a Champions League history question.",
    route: null,
  },
];

function mapBackendMessagesToFrontend(messages) {
  if (!messages || messages.length === 0) {
    return INITIAL_MESSAGES;
  }

  return messages.map((message) => ({
    role: message.role === "bot" ? "bot" : "user",
    text: message.content,
    route: message.route,
  }));
}

function App() {
  const [authMode, setAuthMode] = useState("login");
  const [authEmail, setAuthEmail] = useState("");
  const [authUsername, setAuthUsername] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [authError, setAuthError] = useState("");

  const [token, setToken] = useState(() => {
    return localStorage.getItem("ucl_access_token");
  });

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("ucl_user");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [messages, setMessages] = useState(INITIAL_MESSAGES);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    async function restoreSession() {
      if (!token) return;

      try {
        const data = await getMe(token);
        setUser(data.user);
        localStorage.setItem("ucl_user", JSON.stringify(data.user));

        const historyData = await getChatHistory(token);
        setMessages(mapBackendMessagesToFrontend(historyData.messages));
      } catch (error) {
        localStorage.removeItem("ucl_access_token");
        localStorage.removeItem("ucl_user");
        setToken(null);
        setUser(null);
        setMessages(INITIAL_MESSAGES);
      }
    }

    restoreSession();
  }, [token]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleAuthSubmit(e) {
    e.preventDefault();
    setAuthError("");

    try {
      let data;

      if (authMode === "register") {
        data = await registerUser(authEmail, authUsername, authPassword);
      } else {
        data = await loginUser(authEmail, authPassword);
      }

      localStorage.setItem("ucl_access_token", data.access_token);
      localStorage.setItem("ucl_user", JSON.stringify(data.user));

      setToken(data.access_token);
      setUser(data.user);

      const historyData = await getChatHistory(data.access_token);
      setMessages(mapBackendMessagesToFrontend(historyData.messages));

      setAuthEmail("");
      setAuthUsername("");
      setAuthPassword("");
    } catch (error) {
      setAuthError(error.message);
    }
  }

  async function handleSend(e) {
    e.preventDefault();

    if (!input.trim()) return;
    if (!token) return;

    const userMessage = input.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userMessage, route: null },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(userMessage, token);

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
          text: error.message || "Sorry, something went wrong while contacting the backend.",
          route: "error",
        },
      ]);

      if (error.message.includes("token") || error.message.includes("Authorization")) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  }

  async function clearChat() {
    if (!token) return;

    try {
      await clearChatHistory(token);
      setMessages(INITIAL_MESSAGES);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: error.message || "Failed to clear chat history.",
          route: "error",
        },
      ]);
    }
  }

  function handleLogout() {
    localStorage.removeItem("ucl_access_token");
    localStorage.removeItem("ucl_user");

    setToken(null);
    setUser(null);
    setMessages(INITIAL_MESSAGES);
    setInput("");
  }

  if (!user || !token) {
    return (
      <div className="app">
        <div className="auth-container">
          <img
            src="/ucl-logo.png"
            alt="UEFA Champions League Logo"
            className="auth-logo"
          />

          <h1>Champions League Chatbot</h1>
          <p>Login or register to start chatting.</p>
          <div className="auth-tabs">
            <button
              className={authMode === "login" ? "active" : ""}
              onClick={() => setAuthMode("login")}
            >
              Login
            </button>

            <button
              className={authMode === "register" ? "active" : ""}
              onClick={() => setAuthMode("register")}
            >
              Register
            </button>
          </div>

          <form className="auth-form" onSubmit={handleAuthSubmit}>
            <input
              type="email"
              placeholder="Email"
              value={authEmail}
              onChange={(e) => setAuthEmail(e.target.value)}
              required
            />

            {authMode === "register" && (
              <input
                type="text"
                placeholder="Username"
                value={authUsername}
                onChange={(e) => setAuthUsername(e.target.value)}
                required
              />
            )}

            <input
              type="password"
              placeholder="Password"
              value={authPassword}
              onChange={(e) => setAuthPassword(e.target.value)}
              required
            />

            {authError && <p className="auth-error">{authError}</p>}

            <button type="submit">
              {authMode === "register" ? "Register" : "Login"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <img
            src="/ucl-logox.png"
            alt="UEFA Champions League Logo"
            className="chat-logo"
          />

          <h1>Champions League Chatbot</h1>
          <p>Logged in as {user.username} ({user.email})</p>

          <div className="header-actions">
            <button className="clear-button" onClick={clearChat}>
              Clear Chat
            </button>

            <button className="logout-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
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

          <div ref={messagesEndRef} />
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