const hats = [
  { key: "white", label: "Белая", subtitle: "Факты", color: "bg-slate-100 border-slate-300 text-slate-900" },
  { key: "red", label: "Красная", subtitle: "Эмоции", color: "bg-rose-100 border-rose-300 text-rose-900" },
  { key: "black", label: "Черная", subtitle: "Риски", color: "bg-zinc-200 border-zinc-400 text-zinc-900" },
  { key: "yellow", label: "Желтая", subtitle: "Выгоды", color: "bg-amber-100 border-amber-300 text-amber-900" },
  { key: "green", label: "Зеленая", subtitle: "Улучшения", color: "bg-emerald-100 border-emerald-300 text-emerald-900" },
];

function tryParseJson(text) {
  if (typeof text !== "string") return null;
  const trimmed = text.trim();
  if (!trimmed.startsWith("{") && !trimmed.startsWith("[")) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    return null;
  }
}

function StructuredText({ value }) {
  if (!value) return <p className="mt-2 text-sm opacity-80">—</p>;

  const parsed = tryParseJson(value);
  if (!parsed) {
    return <p className="mt-2 whitespace-pre-wrap text-sm">{String(value)}</p>;
  }

  if (Array.isArray(parsed)) {
    return (
      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
        {parsed.map((item, idx) => (
          <li key={idx}>{typeof item === "string" ? item : JSON.stringify(item, null, 0)}</li>
        ))}
      </ul>
    );
  }

  if (typeof parsed === "object" && parsed) {
    return (
      <div className="mt-2 space-y-2">
        {Object.entries(parsed).map(([k, v]) => (
          <div key={k}>
            <p className="text-xs font-semibold uppercase tracking-wide opacity-80">{k.replaceAll("_", " ")}</p>
            {Array.isArray(v) ? (
              <ul className="mt-1 list-disc space-y-1 pl-5 text-sm">
                {v.map((item, idx) => (
                  <li key={idx}>{typeof item === "string" ? item : JSON.stringify(item, null, 0)}</li>
                ))}
              </ul>
            ) : (
              <p className="mt-1 whitespace-pre-wrap text-sm">{typeof v === "string" ? v : JSON.stringify(v)}</p>
            )}
          </div>
        ))}
      </div>
    );
  }

  return <p className="mt-2 whitespace-pre-wrap text-sm">{String(value)}</p>;
}

function HatCard({ hat, text }) {
  return (
    <div className={`rounded-xl border p-3 ${hat.color}`}>
      <div className="flex items-start gap-3">
        <div className="h-12 w-12 shrink-0 rounded-lg border border-black/10 bg-white/60">
          {/* сюда позже можно подставить <img src="..." alt="..." /> */}
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold">{hat.label} шляпа</p>
          <p className="text-xs opacity-80">{hat.subtitle}</p>
        </div>
      </div>
      <StructuredText value={text} />
    </div>
  );
}

export default function AnalysisPanel({ analysis }) {
  if (!analysis) {
    return <p className="text-sm text-slate-500">Анализ пока не выполнен.</p>;
  }

  return (
    <div className="rounded-2xl bg-slate-50 p-4">
      <div className="mb-4 text-center">
        <h4 className="text-base font-semibold text-slate-900">Анализ по шести шляпам</h4>
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        {hats.slice(0, 3).map((hat) => <HatCard key={hat.key} hat={hat} text={analysis[hat.key]} />)}

        <div className="rounded-2xl border-2 border-blue-300 bg-blue-100 p-4 md:col-span-3">
          <div className="mx-auto flex max-w-3xl items-start gap-3">
            <div className="h-12 w-12 shrink-0 rounded-lg border border-blue-400 bg-white/60" />
            <div className="min-w-0 flex-1">
              <p className="text-sm font-bold text-blue-900">Синяя шляпа (общее мнение)</p>
              <div className="text-blue-900">
                <StructuredText value={analysis.blue} />
              </div>
            </div>
          </div>
        </div>

        {hats.slice(3).map((hat) => <HatCard key={hat.key} hat={hat} text={analysis[hat.key]} />)}
        <div className="hidden md:block" />
      </div>
    </div>
  );
}
