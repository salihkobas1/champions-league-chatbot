export async function sendChatMessage(message, token) {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ message }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to send message");
  }

  return data;
}

export async function getChatHistory(token) {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/chat/history`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch chat history");
  }

  return data;
}

export async function clearChatHistory(token) {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/chat/history`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to clear chat history");
  }

  return data;
}