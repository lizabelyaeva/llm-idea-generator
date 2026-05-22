import { useEffect, useState } from "react";

import { adminApi } from "../services/api";
import {
  clearAdminSession,
  clearLegacyAdminStorage,
  getAdminToken,
} from "../services/adminAuth";

export default function AdminPage() {
  const [view, setView] = useState("checking");
  const [passwordInput, setPasswordInput] = useState("");
  const [authError, setAuthError] = useState(null);

  const [llmModel, setLlmModel] = useState("");
  const [models, setModels] = useState([]);
  const [prompts, setPrompts] = useState({ generation: "", analysis: "", evaluation: "" });
  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  function logout() {
    clearAdminSession();
    setView("login");
    setPasswordInput("");
    setLlmModel("");
    setModels([]);
    setPrompts({ generation: "", analysis: "", evaluation: "" });
    setLogs([]);
    setMessage(null);
    setError(null);
  }

  async function loadPanelData() {
    setLoading(true);
    setError(null);
    try {
      const [settings, promptData, logData] = await Promise.all([
        adminApi.getSettings(),
        adminApi.getPrompts(),
        adminApi.getLogs(),
      ]);
      setLlmModel(settings.llm_model);
      setModels(settings.available_models || []);
      setPrompts({
        generation: promptData.generation,
        analysis: promptData.analysis,
        evaluation: promptData.evaluation,
      });
      setLogs(logData.items || []);
      setView("panel");
    } catch (err) {
      if (String(err.message).includes("401")) {
        logout();
        setAuthError("Сессия администратора истекла. Введите пароль снова.");
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    clearLegacyAdminStorage();

    async function verifyExistingSession() {
      if (!getAdminToken()) {
        setView("login");
        return;
      }
      try {
        await adminApi.verifySession();
        await loadPanelData();
      } catch {
        clearAdminSession();
        setView("login");
      }
    }

    verifyExistingSession();
  }, []);

  async function handleLogin(event) {
    event.preventDefault();
    setAuthError(null);
    try {
      await adminApi.login(passwordInput);
      setPasswordInput("");
      await loadPanelData();
    } catch (err) {
      clearAdminSession();
      setAuthError(err.message);
      setView("login");
    }
  }

  async function saveModel() {
    setMessage(null);
    setError(null);
    try {
      const data = await adminApi.saveSettings({ llm_model: llmModel });
      setLlmModel(data.llm_model);
      setMessage("Модель сохранена");
    } catch (err) {
      setError(err.message);
    }
  }

  async function savePrompts() {
    setMessage(null);
    setError(null);
    try {
      const data = await adminApi.savePrompts(prompts);
      setPrompts({
        generation: data.generation,
        analysis: data.analysis,
        evaluation: data.evaluation,
      });
      setMessage("Промты сохранены");
    } catch (err) {
      setError(err.message);
    }
  }

  if (view === "checking") {
    return (
      <main className="mx-auto max-w-md p-6">
        <p className="text-slate-600">Проверка доступа администратора...</p>
      </main>
    );
  }

  if (view === "login") {
    return (
      <main className="mx-auto max-w-md space-y-6 p-6">
        <header className="space-y-1">
          <h1 className="text-3xl font-bold">Админ-панель</h1>
          <p className="text-slate-600">Отдельный вход администратора.</p>
        </header>

        <div className="rounded-xl bg-white p-6 shadow">
          <h2 className="mb-3 text-xl font-semibold">Вход</h2>
          <form className="space-y-3" onSubmit={handleLogin}>
            <div>
              <label className="mb-1 block text-sm font-medium">Пароль администратора</label>
              <input
                type="password"
                className="w-full rounded-lg border p-2"
                placeholder="ADMIN_PASSWORD"
                value={passwordInput}
                onChange={(e) => setPasswordInput(e.target.value)}
                autoComplete="off"
              />
            </div>
            {authError && (
              <div className="rounded-lg bg-red-100 p-2 text-sm text-red-700">Ошибка: {authError}</div>
            )}
            <button type="submit" className="w-full rounded-lg bg-blue-600 px-4 py-2 text-white">
              Войти в админку
            </button>
          </form>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-6xl space-y-6 p-6">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-3xl font-bold">Админ-панель</h1>
          <p className="text-slate-600">Модель LLM, промты и логи</p>
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 hover:bg-slate-50"
            onClick={loadPanelData}
            disabled={loading}
          >
            Обновить
          </button>
          <button
            type="button"
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 hover:bg-slate-50"
            onClick={logout}
          >
            Выйти
          </button>
        </div>
      </header>

      {message && <div className="rounded-lg bg-green-100 p-3 text-green-800">{message}</div>}
      {error && <div className="rounded-lg bg-red-100 p-3 text-red-700">{error}</div>}

      <section className="rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-lg font-semibold">Настройки модели</h2>
        <div className="flex flex-wrap items-end gap-3">
          <label className="flex min-w-[240px] flex-1 flex-col gap-1 text-sm">
            LLM модель
            <select
              className="rounded-lg border p-2"
              value={llmModel}
              onChange={(e) => setLlmModel(e.target.value)}
            >
              {models.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            className="rounded-lg bg-slate-900 px-4 py-2 text-white"
            onClick={saveModel}
          >
            Сохранить
          </button>
        </div>
      </section>

      <section className="rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-lg font-semibold">Промты</h2>
        <p className="mb-3 text-xs text-slate-500">
          Плейсхолдеры: generation — {"{base_prompt}"}, {"{number_of_ideas}"}; analysis — {"{topic}"},{" "}
          {"{idea_title}"}, {"{idea_description}"}; evaluation — {"{topic}"}, {"{idea_title}"},{" "}
          {"{idea_description}"}, {"{analysis_json}"}.
        </p>
        <div className="space-y-4">
          <label className="block text-sm">
            Генерация
            <textarea
              className="mt-1 h-40 w-full rounded-lg border p-2 font-mono text-xs"
              value={prompts.generation}
              onChange={(e) => setPrompts((p) => ({ ...p, generation: e.target.value }))}
            />
          </label>
          <label className="block text-sm">
            Анализ
            <textarea
              className="mt-1 h-40 w-full rounded-lg border p-2 font-mono text-xs"
              value={prompts.analysis}
              onChange={(e) => setPrompts((p) => ({ ...p, analysis: e.target.value }))}
            />
          </label>
          <label className="block text-sm">
            Оценка
            <textarea
              className="mt-1 h-40 w-full rounded-lg border p-2 font-mono text-xs"
              value={prompts.evaluation}
              onChange={(e) => setPrompts((p) => ({ ...p, evaluation: e.target.value }))}
            />
          </label>
          <button type="button" className="rounded-lg bg-slate-900 px-4 py-2 text-white" onClick={savePrompts}>
            Сохранить промты
          </button>
        </div>
      </section>

      <section className="rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-lg font-semibold">Логи</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b text-slate-500">
                <th className="px-2 py-2">ID</th>
                <th className="px-2 py-2">Действие</th>
                <th className="px-2 py-2">Время</th>
                <th className="px-2 py-2">Детали</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((row) => (
                <tr key={row.id} className="border-b align-top">
                  <td className="px-2 py-2">{row.id}</td>
                  <td className="px-2 py-2">
                    <span
                      className={
                        row.action === "error"
                          ? "rounded bg-red-100 px-2 py-0.5 text-red-700"
                          : "rounded bg-emerald-100 px-2 py-0.5 text-emerald-700"
                      }
                    >
                      {row.action}
                    </span>
                  </td>
                  <td className="px-2 py-2 whitespace-nowrap">
                    {row.timestamp ? new Date(row.timestamp).toLocaleString("ru-RU") : "—"}
                  </td>
                  <td className="max-w-xl px-2 py-2 text-slate-700">{row.details}</td>
                </tr>
              ))}
              {!logs.length && (
                <tr>
                  <td colSpan={4} className="px-2 py-4 text-slate-500">
                    Логов пока нет
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
