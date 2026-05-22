const ADMIN_TOKEN_KEY = "admin_token";

/** Удаляет устаревшие ключи, когда пароль хранился в localStorage. */
export function clearLegacyAdminStorage() {
  localStorage.removeItem("isAdmin");
  localStorage.removeItem("adminPassword");
}

export function getAdminToken() {
  return sessionStorage.getItem(ADMIN_TOKEN_KEY) || "";
}

export function setAdminToken(token) {
  sessionStorage.setItem(ADMIN_TOKEN_KEY, token);
}

export function clearAdminSession() {
  sessionStorage.removeItem(ADMIN_TOKEN_KEY);
}

export function getAdminAuthHeaders() {
  const token = getAdminToken();
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}
