# Case Study: The Paper-to-Live Gap

**Mayur Agrawal | 100xEngineers Cohort 7 | Custom capstone (solo)**
Live: https://www.narviko.com | Workflow: `workflow/paper-live-matcher.workflow.json`

## TL;DR

Retail option traders test strategies on paper, then guess how much real money to put on them.
I ran paper-vs-live reconciliations by hand for two traders. My hypothesis - that 80% of the
rupee gap would get a named cause - failed: 0% and 5.5%. The failure showed where the real
problem is. Paper and live could not even be lined up, and one trader had 4 lots unhedged
without knowing it. Both traders, unprompted, said: check the match first. That changed what I
build: a matcher that pairs every live fill with its planned leg on instrument, quantity and
time, and flags short or missing legs in the same session.

## 1. The problem

I built Narviko, an options-selling engine on Zerodha Kite Connect, and run it alongside my
day job. It has paper-traded since 23 July 2026. Not one rupee has gone live.

Two things stop me. First, I do not know my real slippage, fill rate or signal-to-fill latency.
The engine never recorded them. A good paper record could be half that live, or negative.
Second, the engine's belief and the broker's truth drift, and nothing tells me:

- 26 Aug: the engine entered 3 of 4 legs of a BANKNIFTY batch despite an all-or-nothing gate,
  then halted on a phantom loss (trade book Rs -659, risk book Rs -7,175).
- 27 Aug: the margin gate computed Rs 24,85,855 where the broker priced the same basket at
  Rs 15,09,873, and denied 151 of 154 entries.
- One strategy placed zero orders for 13 sessions. Nothing said so.

I found each of these hours or days later, by reading logs.

## 2. Is it only me? The null test first

Before building anything, I checked whether an LLM plus a skill plus a connector already solves
it. My engine already diffs broker positions against its ledger every 3 seconds. I wrote a
200-line log-tail-to-Telegram pager in one evening, with zero engine changes. That covers
detection on my own engine - so it is tooling, not the capstone.

What no tool covers: the trader's plan lives in their bot, not at the broker. The broker cannot
flag a leg that was planned and never filled, because it never saw the plan.

## 3. Talking to traders

On 14 Sep 2026 I interviewed two retail traders over WhatsApp with 7 Mom-test questions. I told
them the existing alternatives (Kite positions API, Console, OpenAlgo, a scheduled diff script)
before asking if they had the problem.

| | Trader A | Trader B |
|---|---|---|
| Profile | Own trading bot, paper testing, Rs 38.14L capital on sheet | Manual live trader since 2020, also a paper algo |
| Gap number before | None. "7 trades, 4 profitable" | None. "Some slippage or variance ... does happen" |
| Data sent | Sensibull snapshot (12 legs) + paper summary | Live and paper xlsx, 15 positions |

Rule: manual for the user, any tool for me. I reconciled both by hand in Excel.

## 4. What I froze before the data

Hypothesis B: if I reconcile one real session by hand, at least 80% of the rupee gap between
paper and live gets a named cause, and the trader names one decision they would change.
Kill line: under 50%.

Metric: attributed % = sum of |gap| on rows with a cause / sum of |gap| on all rows x 100.
Gross, not net, so causes cannot cancel each other out.

## 5. Results

| User | Gross gap Rs | With a cause Rs | Attributed % |
|---|---|---|---|
| Trader A | 22,884 | 0 | 0% |
| Trader B | 1,54,326 | 8,530 | 5.5% |

**Part 1 failed.** Both below the 50% kill line.
**Part 2 held.** Both named a decision they would change.

Why it failed, step by step (full map in `evidence/09-process-map.md`):

- **Trader A:** his paper side was one total for the day, no price per leg. Nothing to match.
  While checking structures by eye I saw NIFTY at 5 short lots against 1 long lot on each side
  - 4 lots unhedged. He had not noticed: "I was just checking overall pnl in kite."
- **Trader B:** all 15 rows matched on symbol and qty, but had no timestamps. Two NIFTY futures
  rows were 128-130 points off paper and made up 94.5% of his gap. Call them slippage and the
  result is 100%; call them unexplained and it is 5.5%. I reported 5.5% because I do not
  believe a NIFTY future slips 130 points.

## 6. What the users said

Trader A: "For me partial fill wala jyada serious hai. Slippage se profit kam hoga but agar hedge hi
pura nahi laga then risk hi alag ho gaya." (The partial fill is more serious. Slippage cuts
profit, but if the hedge was not fully placed, the risk itself is different.)

Trader B: "If comparison itself wrong then slippage number ka koi meaning nahi hai." (If the
comparison is wrong, the slippage number means nothing.)

I excluded one quote: Trader A's "Yes 100%" to my "would that be useful?" It was a leading question.

## 7. What changed: Version C

I had the hard part in the wrong place. Explaining the gap was not the bottleneck. Matching was.

**Hypothesis C:** if every live fill is first matched to its paper row on instrument, planned
quantity and timestamp, then every short or missing leg is flagged in the same session, and once
timestamps are present at least 80% of the rupee gap gets a named cause.

**Kill:** clean data and still under 50%, or the next 2 traders say a leg mismatch never
happened to them.

The build order follows from that (`workflow/paper-live-matcher.workflow.json`):

1. Ingest Zerodha Console tradebook CSV plus the bot's planned orders. Read-only, no broker keys.
2. Validate: one session, timestamps present, arithmetic checks out.
3. Match on symbol, side and a time window.
4. Leg check: planned vs filled qty per structure. Alert on a short leg.
5. Slippage in Rs, bps and ms - only on matched rows.
6. Attribute each gap row to a cause, then score.

## 8. Learnings

1. **A failed hypothesis is the most useful result I got.** Freezing 80% and 50% before seeing
   data stopped me from moving the goalposts.
2. **Ask for the raw tradebook, not a summary.** Both traders sent position summaries. Next
   time: Console CSV plus bot log, with timestamps.
3. **Users rank risk above money.** I thought slippage mattered most. Both put "does it
   match?" first.
4. **Leading questions inflate validation.** One "Yes 100%" would have looked good. It was not
   evidence.
5. **Build less.** My engine has a backtester, dashboards and 10 strategies, and still 0 live.
   The missing piece was one join between plan and fill.

## 9. What is honest about where this stands

- 2 of 5 validation conversations done, both via 100x. No pricing question asked, no LOI yet.
- The matcher is defined and run by hand; the automated version is weeks 2-3 of the plan.
- My own engine is still paper only. Next: one strategy at 1 lot live beside paper for 20
  sessions. Falsifier: live below 50% of paper means the paper record is fiction.

## 10. Next 4 weeks

- Week 1: 3 more traders, with timestamped tradebooks and an LOI ask.
- Weeks 2-3: build the matcher (CSV upload, match, leg flags, report).
- Weeks 3-5: run it on my engine live at 1 lot and on the 5 traders. Verdict against both
  falsifiers.

Not building: strategy marketplace, order placement for others, new strategies, more backtester.
