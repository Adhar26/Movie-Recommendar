from app.engine.evaluate import load_ratings, split, make_popularity, precision_recall_at_k
from app.engine.content import make_content
from app.engine.itemcf import make_itemcf
from app.engine.hybrid import make_hybrid

train, test = split(load_ratings())
pop = make_popularity(train)
cf = make_itemcf(train)

models = [("Popularity", pop), ("Content", make_content(train)), ("ItemCF", cf)]
models += [(f"Hybrid w={w}", make_hybrid(cf, pop, w)) for w in (0.3, 0.5, 0.7)]

for name, fn in models:
    p, r = precision_recall_at_k(fn, train, test)
    print(f"{name:14} P@10={p:.4f}  R@10={r:.4f}")
