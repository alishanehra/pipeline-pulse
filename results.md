# Results (simulated data)

```
researched    1000
contacted      962
engaged        461
meeting        246
won            108
```

Meeting rate by lead source:
```
  lead_source  accounts  engaged_pct  meeting_pct
     Referral       156         58.3         32.1
 Inbound form       197         51.3         31.5
        Event       151         51.0         29.8
Cold research       496         38.7         17.9
```
Meeting rate by industry:
```
          industry  accounts  engaged_pct  meeting_pct
        Technology       209         48.3         32.1
Financial Services       145         52.4         31.7
        Healthcare       233         48.9         27.0
     Manufacturing       145         46.2         20.0
            Retail       126         38.1         15.9
         Education       142         38.7         14.8
```
Meeting rate by company size:
```
company_size  accounts  engaged_pct  meeting_pct
      51-200       342         47.7         26.6
    201-1000       280         47.5         25.4
       1000+       128         43.0         23.4
        1-50       250         44.0         21.6
```

Priority score (held-out 30%): top quartile meeting rate 32.9% vs overall 26.3% = 1.25x lift

A/B message test (engagement): A 45.4% (n=509) vs B 46.8% (n=491), p = 0.643
Cadence test (engagement): 5-day 46.1% (n=512) vs 2-day 46.1% (n=488), p = 0.997