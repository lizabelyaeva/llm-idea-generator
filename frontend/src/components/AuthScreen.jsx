import { useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import { login, register } from "../features/authSlice";

export default function AuthScreen() {
  const dispatch = useDispatch();
  const { loading, error } = useSelector((s) => s.auth);
  const [mode, setMode] = useState("login"); // login | register
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const title = useMemo(() => (mode === "login" ? "Вход" : "Регистрация"), [mode]);

  return (
    <main className="mx-auto max-w-md space-y-6 p-6">
      <header className="space-y-1">
        <h1 className="text-3xl font-bold">Лаборатория Идей</h1>
        <p className="text-slate-600">Войдите или создайте аккаунт, чтобы сохранять идеи в базе данных.</p>
      </header>

      <div className="rounded-xl bg-white p-6 shadow">
        <div className="mb-4 flex gap-2">
          <button
            type="button"
            className={`rounded-lg px-3 py-1 text-sm ${mode === "login" ? "bg-slate-900 text-white" : "bg-slate-100"}`}
            onClick={() => setMode("login")}
          >
            Вход
          </button>
          <button
            type="button"
            className={`rounded-lg px-3 py-1 text-sm ${mode === "register" ? "bg-slate-900 text-white" : "bg-slate-100"}`}
            onClick={() => setMode("register")}
          >
            Регистрация
          </button>
        </div>

        <h2 className="mb-3 text-xl font-semibold">{title}</h2>

        <form
          className="space-y-3"
          onSubmit={(e) => {
            e.preventDefault();
            const payload = { email, password };
            dispatch(mode === "login" ? login(payload) : register(payload));
          }}
        >
          <div>
            <label className="mb-1 block text-sm font-medium">Почта</label>
            <input className="w-full rounded-lg border p-2" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Пароль</label>
            <input
              type="password"
              className="w-full rounded-lg border p-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <p className="mt-1 text-xs text-slate-500">Минимум 6 символов.</p>
          </div>

          {error && <div className="rounded-lg bg-red-100 p-2 text-sm text-red-700">Ошибка: {error}</div>}

          <button disabled={loading} className="w-full rounded-lg bg-blue-600 px-4 py-2 text-white disabled:opacity-50">
            {loading ? "Подождите..." : title}
          </button>
        </form>
      </div>
    </main>
  );
}
