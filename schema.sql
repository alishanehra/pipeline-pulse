-- Schema used by analysis.py (SQLite). One row per prospect account.
CREATE TABLE accounts (
  account_id TEXT PRIMARY KEY,
  industry TEXT, company_size TEXT, region TEXT, lead_source TEXT,
  message_variant TEXT,        -- A/B test arm
  cadence_days INTEGER,        -- days between follow-ups (2 or 5)
  contacted INTEGER, engaged INTEGER, meeting INTEGER, won INTEGER,
  final_stage TEXT
);

-- Funnel: how many accounts reach each stage?
SELECT COUNT(*) AS researched, SUM(contacted) AS contacted, SUM(engaged) AS engaged,
       SUM(meeting) AS meeting, SUM(won) AS won
FROM accounts;

-- Which segments turn into meetings?
SELECT lead_source, COUNT(*) AS accounts,
       ROUND(100.0 * SUM(meeting) / COUNT(*), 1) AS meeting_pct
FROM accounts GROUP BY lead_source ORDER BY meeting_pct DESC;
