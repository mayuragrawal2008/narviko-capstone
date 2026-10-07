# Custom Capstone Submission - Narviko: The Paper-to-Live Verification Gap

**Cohort:** 100xEngineers C7 | **Track:** Custom capstone (solo)
**Submitted by:** Mayur Agrawal | **Date:** 2026-10-07 (updated from 2026-08-30 draft)
**One-liner:** A profitable paper-trading record is worth Rs 0 until every live fill is matched
to its planned leg and the paper-vs-live gap is attributed. I am building the check that does
that matching, first by hand, then in code.

---

## 1. The 60-second pitch

Retail option traders on Zerodha test a strategy on paper, then have to decide how much real
money to put on it. Nobody I talked to could tell me how far live was from paper, or why. I ran
the comparison by hand on two traders' real positions. I expected the hard part to be naming
the cause of the gap. It was not. The hard part came first: paper and live could not even be
lined up. One trader had 5 short lots against 1 long lot on each side - 4 lots unhedged - and
had not noticed, because he only watched overall P&L. Both said, unprompted: check the match
first. Hypothesis: match every live fill to its planned leg on instrument, quantity and time,
flag short or missing legs when they happen, and once timestamps exist, 80% of the rupee gap
gets a named cause. Under 50% with clean data, or two more traders who never saw a leg
mismatch - I stop.

## 2. Observation (no product in it)

I run an options-selling engine on Zerodha from my day job. It has paper-traded since 23 July
2026. Not one rupee has traded live. Two things stop me. First, I do not know the number that
matters: real slippage, real fill rate, real latency from signal to fill. The engine has never
recorded it. Second, the engine's belief and the broker's truth drift, and nobody tells me.
Dated, from my own logs: on 26 Aug the engine entered 3 of 4 legs of a BANKNIFTY batch despite
an all-or-nothing gate, then day-halted on a phantom loss - trade book minus Rs 659, risk book
minus Rs 7,175, because one strategy's fill was charged to another. On 27 Aug the margin gate
summed per-leg margins to Rs 24,85,855 where the broker priced the identical basket at
Rs 15,09,873, and denied 151 of 154 entries. One strategy placed zero orders in 13 sessions and
nothing said so. I found every one of these hours or days later by reading logs.

Then I checked whether this is only me. On 14 Sep I took two traders' real positions and
reconciled paper against live by hand. Neither had a rupee number for their gap. Neither could
line paper up against live: one had a single paper total for the day with no per-leg price, the
other had no timestamps. And one had an unhedged position he had not noticed.

## 3. Hypothesis and falsifier

**Version B (frozen before data, 14 Sep):** If I reconcile one real session by hand, at least
80% of the Rs gap between paper and live gets a named cause, and the trader names at least one
decision he would change. Kill: under 50%.

**Result: B failed.** Trader A 0%, Trader B 5.5%. Part 2 held: both named a decision they would change.

**Version C (current):** If every live fill is first matched to its paper row on instrument,
planned quantity and timestamp, then in one session every short or missing leg gets flagged
when it happens, and once timestamps are present at least 80% of the Rs gap gets a named cause
(slippage, missed-fill, partial-leg, timing, bot-defect, broker-reject).

**Falsifier:** If the trader's data has timestamps and planned quantity and I still cannot give
a cause to at least 50% of the gap, OR the next 2 traders I talk to say a leg mismatch has never
happened to them, Version C is wrong. Lines are not moved until 2 more people are run.

**Own-capital falsifier (unchanged):** If, over 20 sessions on the same signals, my own live net
P&L is below 50% of paper net P&L, my paper record is fiction and no capital is deployed on it.

## 4. Baseline and target

**Impact metric:** % of the paper-vs-live gap (gross, in Rs) that carries a named cause.

| User | Data | Gross gap Rs | With a cause Rs | Before | After (by hand) | Target |
|---|---|---|---|---|---|---|
| Trader A | 30 Sep 2025 positions, 12 legs | 22,884 | 0 | 0% (no Rs figure) | 0% | 80% |
| Trader B | 15 open positions, no date | 1,54,326 | 8,530 | 0% (by feel) | 5.5% | 80% |

**Leg-match metric (added after Version C):** share of live legs matched to a planned leg within
a time window, and time to flag a short or missing leg.

| Metric | Today | Target |
|---|---|---|
| Trader A's unhedged lots found | 4 lots, found by me days later, by hand | flagged in the same session |
| Time to detect engine-vs-broker drift (my engine) | hours (manual log reads) | under 60 s |
| My live orders placed | 0; realized Rs 0 | 1 strategy at 1 lot, 20 sessions |
| Live / paper ratio on same signals (my engine) | unmeasured | 0.8+ deployable; below 0.5 kill |
| Per-fill slippage, signal-to-fill latency | recorded nowhere | Rs, bps and ms per fill |

## 5. Null test - why an LLM plus skill plus connector does not already do this

Run before committing. Broker-vs-ledger position diffing already exists in my engine (every
3 s, detect-only). I built the cheap version in one evening: a 200-line log-tail-to-Telegram
script, zero engine changes, tested (`tools/null_test_parity.py`). That covers detection on my
own engine, so it is tooling, not the capstone.

Both users were told the alternatives before validation (Q6: Kite positions API, Console,
OpenAlgo P&L page, a scheduled diff script). Trader A: "I think there is still room for improvement.
I would prefer ... an AI agent that can read the raw trading data, compare expected vs actual
trades, and automatically identify differences." What no existing tool gives: a join of the
trader's planned legs (which live in their bot, not at the broker) against broker fills on
instrument, qty and time. The broker never sees the plan, so it cannot flag a leg that was
planned and never filled.

## 6. Validation - conversations (outside friends and family)

Method: 7 Mom-test questions over WhatsApp, alternatives disclosed (Q6), then a manual
reconciliation sent back and a reaction collected. Evidence: `MayurAgrawal_FirstAction/`
(interview notes, 4 timestamped screenshots, reconciliations, process map).

| # | Person | Channel | Paper-vs-live number before | What I found by hand | Capital | Decision they changed |
|---|---|---|---|---|---|---|
| 1 | Trader A (100x Fellow, own trading bot, paper) | WhatsApp, 14 Sep | None ("7 trades, 4 profitable") | Rs 22,884 gap (paper Rs 65,517 vs real Rs 42,633); 4 NIFTY lots unhedged, unnoticed | Rs 38.14L on his sheet; decides own capital | "Before increasing real money I'll definitely check that all legs match the expected qty." |
| 2 | Trader B (100x Fellow, manual live since 2020, paper algo) | WhatsApp, 14 Sep | None ("some slippage ... does happen") | Rs 1,54,326 gross gap; 94.5% on 2 NIFTY futures rows, 128-130 pts off | Not asked | Fix the futures price source first; if the gap is real, change order type or entry logic |
| 3 | PENDING | | | | | |
| 4 | PENDING | | | | | |
| 5 | PENDING | | | | | |

Honest gaps: 2 of 5 done. Both came through 100x. No pricing question asked yet, no LOI yet.
Trader A's "Yes 100%" to "would that be useful?" is excluded - it was a leading question.
Next: 3 more traders who run multi-leg strategies with real money, at least one with a budget,
asked what they already spend on tools (not what they would pay), and an LOI ask.

## 7. What gets built (v1, 4-5 weeks) - and what does not

**Done:** observation, numbers, null test, parity pager script, two manual reconciliations,
Version B tested and failed, Version C written with its kill line.
**Week 1:** 3 more traders, run by hand. Ask for Console tradebook CSV plus the bot's planned
orders, with timestamps this time.
**Weeks 2-3:** the matcher - read-only upload of Zerodha Console tradebook CSV plus planned
orders; match on instrument, planned qty and time window; flag short or missing legs; only
matched rows get a slippage number. No broker access needed. My engine already has a
tradebook importer.
**Weeks 3-5:** run it on my own engine with one strategy live at 1 lot beside paper (20
sessions), plus the 5 traders' data. Verdict against both falsifiers; case study; demo video.

Explicitly NOT built: strategy marketplace, placing orders for other people, new strategies,
more backtester work, a public product before the manual version works for 5 people.

## 8. Impact - measured by someone other than me

Every result line traces to a Zerodha contract note or the trader's own files. A stranger needs
no access to my code: the tradebook plus the planned orders settle it. For traders: a missed
hedge caught the same session instead of days later (Trader A's 4 lots). For me: a live-vs-paper
ratio that decides whether my paper record is deployable, on a measured basis.

## 9. Deliverables mapping

| Required | What I submit |
|---|---|
| Live project link | https://www.narviko.com (my engine, paper only) plus the matcher report page when built |
| GitHub repo / workflow | Capstone repo: matcher, attribution report, parity pager (engine stays private; interfaces documented) |
| Demo video | Upload tradebook plus planned orders, see a short leg flagged and the gap attributed |
| Case study | TL;DR, problem, why Version B failed, Version C, results table with measured column filled |

## 10. Self-check (office-hour doc, all eight)

1. Observation without product - section 2. PASS.
2. Mine - my engine, my Rs 0 live, my logs. PASS.
3. 60 seconds - section 1. PASS (read aloud before submit).
4. Falsifier - section 3, Version C kill line. PASS.
5. Baseline number - section 4, 0% / 0% and 0% / 5.5%, measured by hand. PASS.
6. Null test - section 5, cheap version built, alternatives disclosed to users. PASS.
7. Five outside validators, one controls budget - 2 of 5. PARTIAL. No LOI yet.
8. Manual first - delivered by hand to 2 people on 14 Sep. PASS.
