import { useEffect, useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import IdeaCard from "./components/IdeaCard";
import IdeaForm from "./components/IdeaForm";
import { analyzeIdea, deleteIdea, generatePipeline, refreshIdeas, saveIdea, scoreIdea } from "./features/ideasSlice";

export default function App() {
  const dispatch = useDispatch();
  const { items, loading, error } = useSelector((state) => state.ideas);
  const [expandedSessionIds, setExpandedSessionIds] = useState({});

  useEffect(() => {
    dispatch(refreshIdeas());
  }, [dispatch]);

  const groupedBySession = useMemo(() => {
    const map = new Map();
    for (const idea of items) {
      const key = idea.session_id;
      if (!map.has(key)) {
        map.set(key, {
          sessionId: idea.session_id,
          topic: idea.session_topic || "Без темы",
          ideas: [],
        });
      }
      map.get(key).ideas.push(idea);
    }
    return Array.from(map.values());
  }, [items]);

  return (
    <main className="mx-auto max-w-6xl space-y-6 p-6">
      <header>
        <h1 className="text-3xl font-bold">Лаборатория Идей</h1>
        <p className="text-slate-600">
          Структурированная генерация, анализ по шести шляпам, оценка и ранжирование идей.
        </p>
      </header>

      <IdeaForm
        loading={loading}
        onSubmit={(payload) => {
          dispatch(generatePipeline(payload));
        }}
      />

      {error && <div className="rounded-lg bg-red-100 p-3 text-red-700">Ошибка: {error}</div>}

      <section>
        <h2 className="mb-4 text-2xl font-semibold">Список идей по темам</h2>
        <div className="space-y-3">
          {groupedBySession.map((sessionGroup) => {
            const isExpanded = expandedSessionIds[sessionGroup.sessionId] ?? true;
            return (
              <div key={sessionGroup.sessionId} className="rounded-xl border border-slate-200 bg-white shadow-sm">
                <button
                  className="flex w-full items-center justify-between px-4 py-3 text-left"
                  onClick={() =>
                    setExpandedSessionIds((prev) => ({
                      ...prev,
                      [sessionGroup.sessionId]: !isExpanded,
                    }))
                  }
                >
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">Тема</p>
                    <p className="text-base font-semibold text-slate-900">{sessionGroup.topic}</p>
                  </div>
                  <div className="text-sm text-slate-600">
                    {sessionGroup.ideas.length} идей • {isExpanded ? "Скрыть" : "Показать"}
                  </div>
                </button>

                {isExpanded && (
                  <div className="grid gap-4 border-t border-slate-100 p-4">
                    {sessionGroup.ideas.map((idea) => (
                      <IdeaCard
                        key={idea.id}
                        idea={idea}
                        onDelete={(id) => dispatch(deleteIdea(id))}
                        onSave={(ideaData) => dispatch(saveIdea(ideaData))}
                        onAnalyze={(id) => dispatch(analyzeIdea(id))}
                        onScore={(id) => dispatch(scoreIdea(id))}
                      />
                    ))}
                  </div>
                )}
              </div>
            );
          })}

          {!groupedBySession.length && (
            <p className="text-slate-500">Пока нет идей. Запустите генерацию выше.</p>
          )}
        </div>
      </section>
    </main>
  );
}
