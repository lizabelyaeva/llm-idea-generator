import { Bar } from "react-chartjs-2";
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function ScoreChart({ score }) {
  if (!score) {
    return <p className="text-sm text-slate-500">Оценка пока не выполнена.</p>;
  }

  const data = {
    labels: ["Новизна", "Реализуемость", "Полезность"],
    datasets: [
      {
        label: "Оценка",
        data: [score.novelty, score.feasibility, score.usefulness],
        backgroundColor: ["#60a5fa", "#34d399", "#fbbf24"],
      },
    ],
  };

  return (
    <div>
      <Bar data={data} options={{ responsive: true, plugins: { legend: { display: false } }, scales: { y: { min: 0, max: 10 } } }} />
      <p className="mt-2 text-sm font-semibold">Итоговый балл: {score.total}</p>
    </div>
  );
}
