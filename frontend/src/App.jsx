import { useState, useEffect } from "react";

function Card({ m, dataset, onRate }) {
  const [ok, setOk] = useState(true);
  return (
    <div className="card">
      {ok ? (
        <img src={`/api/poster/${m.id}?dataset=${dataset}`} alt="" onError={() => setOk(false)} />
      ) : (
        <div className="noimg">{m.title}</div>
      )}
      <div className="title">{m.title}</div>
      <div className="genres">{(m.genres || "").split("|").join(", ")}</div>
      <div className="stars">
        {[1, 2, 3, 4, 5].map((s) => (
          <button key={s} onClick={() => onRate(m.id, s)}>{s}</button>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [dataset, setDataset] = useState("movies");
  const [user, setUser] = useState("1");
  const [q, setQ] = useState("");
  const [title, setTitle] = useState("");
  const [items, setItems] = useState([]);
  const [status, setStatus] = useState("");

  const loadRecs = async (ds = dataset) => {
    setStatus(ds === "anime" ? "Loading anime model (first time takes about a minute)..." : "");
    const r = await fetch(`/api/recommendations/${user}?n=20&dataset=${ds}`);
    setItems(await r.json());
    setTitle("Recommended for you");
    setStatus("");
  };

  const search = async () => {
    if (!q.trim()) return;
    const r = await fetch(`/api/search?q=${encodeURIComponent(q)}&dataset=${dataset}`);
    setItems(await r.json());
    setTitle(`Results for "${q}"`);
  };

  const rate = async (id, rating) => {
    await fetch("/api/rate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: Number(user), movie_id: id, rating, dataset }),
    });
    setStatus(`Saved ${rating} stars. Click Retrain to update recommendations.`);
  };

  const retrain = async () => {
    await fetch(`/api/retrain?dataset=${dataset}`, { method: "POST" });
    setStatus("Retraining... recommendations reload in a few seconds.");
    setTimeout(() => { loadRecs(); setStatus("Recommendations updated."); }, 10000);
  };

  const switchTo = (ds) => {
    setDataset(ds);
    setItems([]);
    loadRecs(ds);
  };

  useEffect(() => { loadRecs(); }, []);

  return (
    <div className="wrap">
      <div className="bar">
        <button onClick={() => switchTo("movies")} style={{ background: dataset === "movies" ? "#e50914" : "#222" }}>Movies</button>
        <button onClick={() => switchTo("anime")} style={{ background: dataset === "anime" ? "#e50914" : "#222" }}>Anime</button>
        <input value={user} onChange={(e) => setUser(e.target.value)} style={{ width: 60 }} />
        <button onClick={() => loadRecs()}>Load</button>
        <input
          placeholder={`Search ${dataset}...`}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && search()}
          style={{ flex: 1, minWidth: 160 }}
        />
        <button onClick={retrain}>Retrain</button>
      </div>
      <h2>{title}</h2>
      <div className="row">
        {items.map((m) => <Card key={`${dataset}-${m.id}`} m={m} dataset={dataset} onRate={rate} />)}
      </div>
      <p>{status}</p>
    </div>
  );
}