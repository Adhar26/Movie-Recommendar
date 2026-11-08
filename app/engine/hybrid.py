def make_hybrid(cf, pop, w=0.5, k=60):
    def recommend(user_id, seen):
        a = cf(user_id, seen)
        b = pop(user_id, seen)
        if not a:
            return b          # cold start: fall back to popularity
        scores = {}
        for rank, m in enumerate(a):
            scores[m] = scores.get(m, 0) + w / (k + rank)
        for rank, m in enumerate(b):
            scores[m] = scores.get(m, 0) + (1 - w) / (k + rank)
        return sorted(scores, key=scores.get, reverse=True)
    return recommend
