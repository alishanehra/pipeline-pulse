"""Generate a SIMULATED B2B prospect dataset. No real companies or people are used."""
import numpy as np, pandas as pd

rng = np.random.default_rng(42)
N = 1000
sig = lambda x: 1 / (1 + np.exp(-x))

df = pd.DataFrame({
    "account_id": [f"A{i:04d}" for i in range(1, N + 1)],
    "industry": rng.choice(["Healthcare", "Technology", "Manufacturing", "Financial Services", "Education", "Retail"], N, p=[.22, .22, .15, .15, .13, .13]),
    "company_size": rng.choice(["1-50", "51-200", "201-1000", "1000+"], N, p=[.25, .35, .28, .12]),
    "region": rng.choice(["Texas", "Southeast", "Northeast", "Midwest", "West"], N),
    "lead_source": rng.choice(["Cold research", "Referral", "Event", "Inbound form"], N, p=[.5, .15, .15, .2]),
    "message_variant": rng.choice(["A", "B"], N),
    "cadence_days": rng.choice([2, 5], N),
})

# Assumed effects used ONLY to simulate behavior (these are my assumptions, not real findings)
ind = {"Healthcare": .35, "Technology": .15, "Manufacturing": -.1, "Financial Services": .05, "Education": -.2, "Retail": -.25}
size = {"1-50": -.2, "51-200": .2, "201-1000": .25, "1000+": -.15}
src = {"Cold research": -.25, "Referral": .6, "Event": .2, "Inbound form": .5}
base = (-.5 + df.industry.map(ind) + df.company_size.map(size) + df.lead_source.map(src)
        + np.where(df.message_variant == "B", .3, 0) + np.where(df.cadence_days == 2, .15, 0))

u = lambda: rng.random(N)
df["contacted"] = (u() < .95).astype(int)
df["engaged"] = ((u() < sig(base)) & (df.contacted == 1)).astype(int)
df["meeting"] = ((u() < sig(.6 * base + .1)) & (df.engaged == 1)).astype(int)
df["won"] = ((u() < sig(.5 * base - .3)) & (df.meeting == 1)).astype(int)
df["final_stage"] = np.select([df.won == 1, df.meeting == 1, df.engaged == 1, df.contacted == 1],
                              ["Closed won", "Meeting", "Engaged", "Contacted"], "Researched")
df.to_csv("data/accounts.csv", index=False)
print(f"Wrote data/accounts.csv ({len(df)} simulated accounts)")
