import AnalysisPanel from "./AnalysisPanel";
import ScoreChart from "./ScoreChart";

export default function IdeaCard({ idea, onDelete, onSave, onAnalyze, onScore }) {
  return (
    <article className="rounded-xl bg-white p-5 shadow">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-lg font-semibold">
          #{idea.rank || "-"} {idea.title}
        </h3>
        <div className="space-x-2">
          <button className="rounded bg-emerald-600 px-3 py-1 text-sm text-white" onClick={() => onSave(idea)}>
            сохранить
          </button>
          <button className="rounded bg-rose-600 px-3 py-1 text-sm text-white" onClick={() => onDelete(idea.id)}>
            удалить
          </button>
        </div>
      </div>
      <p className="mb-4 text-slate-700">{idea.description}</p>

      <div className="mb-4 flex flex-wrap gap-2">
        <button className="rounded bg-slate-700 px-3 py-1 text-sm text-white" onClick={() => onAnalyze(idea.id)}>
          Обновить анализ
        </button>
        <button className="rounded bg-blue-700 px-3 py-1 text-sm text-white" onClick={() => onScore(idea.id)}>
          Пересчитать оценку
        </button>
      </div>

      <AnalysisPanel analysis={idea.analysis} />
      <div className="mt-4">
        <ScoreChart score={idea.score} />
      </div>
    </article>
  );
}
