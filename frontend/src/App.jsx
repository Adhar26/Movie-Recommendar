import { useState, useEffect } from "react";

function Card({ m, onRate }) {
  const [ok, setOk] = useState(true);
  return (
    <div className="card">
      {ok ? (
        <img src={`/api/poster/${m.id}`} alt="" onError={() => setOk(false)} />
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
  const [user, setUser] = useState("1");
  const [q, setQ] = useState("");
  const [title, setTitle] = useState("");
  const [movies, setMovies] = useState([]);
  const [status, setStatus] = useState("");
  const [animeOnly, setAnimeOnly] = useState(false);
  const [showingSearch, setShowingSearch] = useState(false);

  const loadRecs = async (filterAnime = animeOnly) => {
    const r = await fetch(`/api/recommendations/${user}?n=20&anime=${filterAnime}`);
    setMovies(await r.json());
    setShowingSearch(false);
    setTitle(filterAnime ? "Anime / animation recommendations" : "Recommended for you");
  };

  const search = async (filterAnime = animeOnly) => {
    if (!q.trim()) return;
    const r = await fetch(`/api/search?q=${encodeURIComponent(q)}&anime=${filterAnime}`);
    setMovies(await r.json());
    setShowingSearch(true);
    setTitle(`Results for "${q}"${filterAnime ? " (anime / animation)" : ""}`);
  };

  const toggleAnime = (enabled) => {
    setAnimeOnly(enabled);
    if (showingSearch && q.trim()) search(enabled);
    else loadRecs(enabled);
  };

  const rate = async (movieId, rating) => {
    await fetch("/api/rate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: Number(user), movie_id: movieId, rating }),
    });
    setStatus(`Saved ${rating} stars. Click Retrain to update recommendations.`);
  };

  const retrain = async () => {
    await fetch("/api/retrain", { method: "POST" });
    setStatus("Retraining... recommendations reload in a few seconds.");
    setTimeout(() => { loadRecs(); setStatus("Recommendations updated."); }, 8000);
  };

  useEffect(() => { loadRecs(); }, []);

  return (
    <div className="wrap">
      <div className="bar">
        <input value={user} onChange={(e) => setUser(e.target.value)} style={{ width: 60 }} />
        <button onClick={loadRecs}>Load</button>
        <label className="anime-toggle" title="Filters to titles tagged Animation in MovieLens">
          <input
            type="checkbox"
            checked={animeOnly}
            onChange={(e) => toggleAnime(e.target.checked)}
          />
          Anime / animation
        </label>
        <input
          placeholder="Search movies..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && search()}
          style={{ flex: 1, minWidth: 160 }}
        />
        <button onClick={retrain}>Retrain</button>
      </div>
      <h2>{title}</h2>
      <div className="row">
        {movies.map((m) => <Card key={m.id} m={m} onRate={rate} />)}
      </div>
      <p>{status}</p>
    </div>
  );
}
