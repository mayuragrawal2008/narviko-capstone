# 2. Impact Metric

**% of the paper-vs-live P&L gap (in Rs) that I can put a named cause on.**

For each row: gap = live cash - paper cash. Then:

    attributed % = sum of |gap| on rows with a cause / sum of |gap| on all rows x 100

I divide by the gross gap (sum of the absolute row gaps), not the net. Causes can cancel each
other in the net - a missed hedge can make live look better while slippage makes it worse - and
then the % goes over 100.

Causes I allow: `slippage`, `missed-fill`, `partial-leg`, `timing`, `bot-defect`,
`broker-reject`, `unexplained`. Anything tagged `unexplained` doesn't count.

Paper = the price the strategy expected. Live = what the broker actually filled.

## Before (from the interviews)

| User | What they said | Before |
|---|---|---|
| Trader A | "So far, I have tested 7 trades, and 4 of them were profitable." Causes only as "market volatility and order/execution restrictions." | 0% - no Rs figure for the gap |
| Trader B | "So some slippage or variance in buy price does happen." | 0% - handled by feel, no number |

## After (from my hand reconciliation)

| User | Data | Gross gap Rs | With a cause Rs | Attributed % | Unexplained Rs |
|---|---|---|---|---|---|
| Trader A | 30 Sep 2025 positions | 22,884 (one day total) | 0 | 0% | 22,884 |
| Trader B | 15 open positions, no date given | 1,54,326 | 8,530 | 5.5% | 1,45,796 |

## Measured once, by hand

Trader A went from 0% to 0%. His paper side was one total for the day, so there was nothing to put a
cause on. Trader B went from 0% to 5.5%. The options slippage got a cause; the two NIFTY futures rows,
94.5% of his gap, didn't.

Both are well under what I hoped for (80%). The reason is the same for both and it's in
`10-bottleneck.md`.
