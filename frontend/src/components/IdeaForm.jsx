import { useState } from "react";

export default function IdeaForm({ onSubmit, loading }) {
  const [topic, setTopic] = useState("");
  const [description, setDescription] = useState("");
  const [numberOfIdeas, setNumberOfIdeas] = useState(5);

  return (
    <form
      className="rounded-xl bg-white p-6 shadow"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({
          topic,
          description,
          number_of_ideas: Number(numberOfIdeas),
        });
      }}
    >
      <h2 className="mb-4 text-xl font-semibold">Новая сессия генерации идей</h2>
      <label className="mb-2 block text-sm font-medium">Тема *</label>
      <input
        className="mb-4 w-full rounded-lg border p-2"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        required
      />

      <label className="mb-2 block text-sm font-medium">Описание (необязательно)</label>
      <textarea
        className="mb-4 w-full rounded-lg border p-2"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <label className="mb-2 block text-sm font-medium">Количество идей</label>
      <input
        type="number"
        min={1}
        max={15}
        className="mb-4 w-full rounded-lg border p-2"
        value={numberOfIdeas}
        onChange={(e) => setNumberOfIdeas(e.target.value)}
      />

      <button
        disabled={loading}
        className="rounded-lg bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
        type="submit"
      >
        {loading ? "Генерация..." : "Сгенерировать и проанализировать"}
      </button>
    </form>
  );
}
