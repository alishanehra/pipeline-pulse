"""Pipeline Pulse analysis: funnel, segments, a simple priority score, and an A/B test."""
import sqlite3
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv("data/accounts.csv")
con = sqlite3.connect(":memory:")
df.to_sql("accounts", con, index=False)

funnel = pd.read_sql("""SELECT COUNT(*) AS researched, SUM(contacted) AS contacted, SUM(engaged) AS engaged,
                        SUM(meeting) AS meeting, SUM(won) AS won FROM accounts""", con).iloc[0]

def seg(col):
    return pd.read_sql(f"""SELECT {col}, COUNT(*) AS accounts,
        ROUND(100.0*SUM(engaged)/COUNT(*),1) AS engaged_pct,
        ROUND(100.0*SUM(meeting)/COUNT(*),1) AS meeting_pct
        FROM accounts GROUP BY {col} ORDER BY meeting_pct DESC""", con)
by_src, by_ind, by_size = seg("lead_source"), seg("industry"), seg("company_size")

# Priority score: average historical meeting rate of an account's segments, learned on a 70% train split
rng = np.random.default_rng(1)
idx = rng.permutation(len(df)); cut = int(.7 * len(df))
train, test = df.iloc[idx[:cut]].copy(), df.iloc[idx[cut:]].copy()
feats = ["industry", "company_size", "lead_source"]
rates = {f: train.groupby(f)["meeting"].mean() for f in feats}
test["score"] = np.mean([test[f].map(rates[f]) for f in feats], axis=0)
test["tier"] = pd.qcut(test["score"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
tier = test.groupby("tier", observed=True)["meeting"].mean() * 100
overall = test["meeting"].mean() * 100
lift = tier.iloc[-1] / overall

def ab(col, a, b, metric):
    x, y = df[df[col] == a][metric], df[df[col] == b][metric]
    p1, p2, n1, n2 = x.mean(), y.mean(), len(x), len(y)
    p = (x.sum() + y.sum()) / (n1 + n2)
    z = (p2 - p1) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return p1 * 100, p2 * 100, 2 * norm.sf(abs(z)), n1, n2
msg = ab("message_variant", "A", "B", "engaged")
cad = ab("cadence_days", 5, 2, "engaged")

# Charts
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.barh(funnel.index[::-1], funnel.values[::-1], color="#2B645D")
for i, v in enumerate(funnel.values[::-1]): ax.text(v + 8, i, str(int(v)), va="center")
ax.set_title("Simulated pipeline funnel (1,000 accounts)"); plt.tight_layout(); plt.savefig("charts/funnel.png", dpi=150); plt.close()
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
for a, d, c, t in [(axs[0], by_src, "lead_source", "Meeting rate by lead source (%)"), (axs[1], by_ind, "industry", "Meeting rate by industry (%)")]:
    a.barh(d[c][::-1], d["meeting_pct"][::-1], color="#E9A114"); a.set_title(t)
plt.tight_layout(); plt.savefig("charts/segments.png", dpi=150); plt.close()
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(tier.index.astype(str), tier.values, color="#3E7F76"); ax.axhline(overall, color="#10302D", ls="--", label=f"Overall {overall:.1f}%")
ax.set_title("Held-out test: meeting rate by priority-score tier (%)"); ax.legend(); plt.tight_layout(); plt.savefig("charts/score_tiers.png", dpi=150); plt.close()

lines = ["# Results (simulated data)", "", "```", funnel.astype(int).to_string(), "```", "",
 "Meeting rate by lead source:", "```", by_src.to_string(index=False), "```", "Meeting rate by industry:", "```", by_ind.to_string(index=False), "```",
 "Meeting rate by company size:", "```", by_size.to_string(index=False), "```", "",
 f"Priority score (held-out 30%): top quartile meeting rate {tier.iloc[-1]:.1f}% vs overall {overall:.1f}% = {lift:.2f}x lift", "",
 f"A/B message test (engagement): A {msg[0]:.1f}% (n={msg[3]}) vs B {msg[1]:.1f}% (n={msg[4]}), p = {msg[2]:.3f}",
 f"Cadence test (engagement): 5-day {cad[0]:.1f}% (n={cad[3]}) vs 2-day {cad[1]:.1f}% (n={cad[4]}), p = {cad[2]:.3f}"]
open("results.md", "w").write("\n".join(lines)); print("\n".join(lines))
