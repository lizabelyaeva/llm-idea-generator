const API_URL = "http://localhost:8000";

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (error) {
    throw new Error("Не удалось подключиться к backend (проверьте запуск сервера и URL API)");
  }
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "Ошибка запроса к серверу");
  }
  return response.json();
}

export const api = {
  generateIdeas(payload) {
    return request("/generate", { method: "POST", body: JSON.stringify(payload) });
  },
  getIdeas(sessionId) {
    const query = sessionId ? `?session_id=${sessionId}` : "";
    return request(`/ideas${query}`);
  },
  analyzeIdea(ideaId) {
    return request("/analyze", { method: "POST", body: JSON.stringify({ idea_id: ideaId }) });
  },
  scoreIdea(ideaId) {
    return request("/score", { method: "POST", body: JSON.stringify({ idea_id: ideaId }) });
  },
  deleteIdea(ideaId) {
    return request(`/ideas/${ideaId}`, { method: "DELETE" });
  },
};
