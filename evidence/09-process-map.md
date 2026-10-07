# 9. Process Map

What I actually did, in order, for both users.
D = a fixed rule or formula. P = a judgment call. H = needed the person.

| # | Step | D/P/H | Trader A | Trader B | What went wrong | Narviko today |
|---|---|---|---|---|---|---|
| 1 | Sent 7 questions on WhatsApp, got written answers | H | 12:57 -> 13:09 | 14:28 -> 14:35 | Trader B said "never tried algo trading", then later said he runs one on paper | - |
| 2 | Asked for one session's live fills and what the strategy expected | H | Said no at first, then sent a Sensibull snapshot + 2 xlsx | Sent 2 xlsx (live, paper) | Neither sent a broker tradebook or a bot log. Both sent position summaries | - |
| 3 | Put the live positions in one sheet, one row per leg | D | 12 legs typed from the snapshot | 15 rows, already in xlsx | Trader A's typed sheet has 2026 expiries, the snapshot says 2025 | Positions, order book |
| 4 | Checked the arithmatic: qty x (price - entry) per row, total vs their total | D | Passed, +42,633 matches | 3 rows wrong in his sheet (Rs 21), used my numbers | Trader B's own sheet had P&L mistakes | P&L page |
| 5 | Matched each live row to its paper row | D | **Couldn't.** Paper file is a picture of columns J-P, no price per leg | 15 of 15 matched on symbol + qty, but no times | Trader A's % stuck at 0 | **Missing** - paper and live are separate views |
| 6 | Worked out slippage Rs and bps per row | D | Not possible | Options 40-120 bps, futures ~130 NIFTY points | No times from either, so no latency | Monitors shows latency, not slippage per fill |
| 7 | Checked each structure: planned lots vs filled lots | P | Saw NIFTY 5 short vs 1 long per side, asked Trader A, he confirmed a partial fill | All single legs, nothing to check | I only caught it by looking. There was no planned qty anywhere in the data | **Missing** - no expected vs filled check |
| 8 | Gave each gap row a cause | P | Couldn't tag anything, the gap is one day total | Options = `slippage`, futures = `unexplained` | Hardest step. The 2 futures rows decide 94.5% of the result: call them slippage and it's 100%, call them unexplained and it's 5.5% | **Missing** |
| 9 | Checked the data was one session | P | Yes, 30 Sep 2025 | No - expiries from Sep 2025 to Jun 2026 | Trader B's rows are probably from several days | - |
| 10 | Wrote up the 3 biggest things in plain words | P | BANKNIFTY 70% of P&L, NIFTY partial fill, 55000 PE loss | Oct future 63% of the gap, Sep future win to loss, options Rs 8,530 | - | - |
| 11 | Sent it, asked what surprised them, followed up | H | Summary at 16:18, replies 16:27 - 16:34 | Sent 15:55, replies 16:10 - 16:11 | My "would that be useful?" to Trader A was leading, so I dropped his answer to it | - |

Time: Trader B about 50 minutes for steps 3-10. Trader A I didn't time.

## Where it went wrong

- **Step 5, Trader A:** no paper price per leg, so there was nothing to match. The metric couldn't
  move off 0%.
- **Step 8, Trader B:** one call on 2 rows swings the answer between 5.5% and 100%. Without timestamps
  a cause is really a guess.
- **Step 7:** the most serious thing I found all weekend - Trader A's missing hedge, 4 lots on each
  side - I found by eye, not by any rule. He hadn't seen it.

4 D steps, 4 P steps, 3 H steps. The D steps were quick when the data had the right columns and
impossible when it didn't.
