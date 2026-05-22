import { useEffect, useRef, useState } from "react";
import { useDispatch } from "react-redux";

import { logout } from "../features/authSlice";

export default function UserMenu({ email }) {
  const dispatch = useDispatch();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function onClickOutside(e) {
      if (!ref.current) return;
      if (!ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  const initial = (email || "?").trim().slice(0, 1).toUpperCase();

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white"
        onClick={() => setOpen((v) => !v)}
        title={email}
      >
        {initial}
      </button>
      {open && (
        <div className="absolute right-0 mt-2 w-64 rounded-xl border bg-white p-3 shadow">
          <p className="text-xs uppercase tracking-wide text-slate-500">Аккаунт</p>
          <p className="mb-3 truncate text-sm font-semibold">{email}</p>
          <button
            type="button"
            className="w-full rounded-lg bg-rose-600 px-3 py-2 text-sm text-white"
            onClick={() => dispatch(logout())}
          >
            Выйти
          </button>
        </div>
      )}
    </div>
  );
}
