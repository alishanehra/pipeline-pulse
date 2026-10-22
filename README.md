# Pipeline Pulse

**Which prospects should a sales team contact first?** A simulated B2B sales pipeline, analyzed with Python and SQL.

> **All data is simulated.** No real companies, people, or customer data are used. The numbers below describe my simulated dataset and are not real-world findings. I built it to practice the workflow I use at Toro Intelligence: researching accounts, segmenting them, and tracking them through pipeline stages.

## What it does
1. `generate_data.py` creates 1,000 fake accounts with an industry, company size, region, lead source, outreach message (A or B), and follow-up cadence (2 or 5 days), then simulates how far each account moves through the funnel.
2. `schema.sql` defines the table and the core SQL queries (funnel and segment conversion).
3. `analysis.py` loads the data into SQLite, runs the SQL, builds a simple priority score on a 70% training split, checks it on the held-out 30%, and tests the two A/B questions.

## Results (from the simulated data)
- **Funnel:** 1,000 researched, 962 contacted, 461 engaged, 246 meetings, 108 closed won.
- **Lead source matters most:** referral, inbound, and event accounts reached a meeting 30-32% of the time, versus 17.9% for cold research.
- **Priority score:** on the held-out accounts, the top quartile reached a meeting 32.9% of the time versus 26.3% overall, a 1.25x lift. That is modest, and the test set is small (300 accounts).
- **A/B test (message A vs B):** engagement was 45.4% vs 46.8%, p = 0.64. **No significant difference.** With about 500 accounts per group, I could only detect a large gap.
- **Cadence test (5-day vs 2-day):** 46.1% vs 46.1%, p = 0.997. No difference.

## Limitations
The data is simulated from effects I assumed, so the segment patterns are expected by construction. The point of the project is the method: SQL for funnels, a train/test check on the score, and honest A/B testing with sample size in mind. Next step: rerun it on a real, anonymized pipeline export.

## Run it
```
pip install -r requirements.txt
python generate_data.py
python analysis.py
```
Charts are saved in `charts/` and the full output in `results.md`.
