# 3. Hypothesis

## Version A - my original capstone hypothesis (Aug 2026, about my own engine)

If I run one strategy live at minimum lot size next to the paper book, on the same signals, and
check every fill against the broker within seconds - price, qty, legs, timing - then in 20 trading
sessions I'll have a live return a stranger can verify from contract notes, with every rupee of
paper-vs-live difference given a cause.

- Kill condition: live net P&L below 50% of paper over 20 sessions. Then the paper record is
  fiction and no capital goes on it.

## Version B - for this weekend (frozen before I saw any data)

If I take one real session from a retail algo trader and reconcile it by hand, at least **80%** of
the Rs gap between paper and live will get a named cause, and the trader will name at least
**one** decision they'd change because of it.

- Kill condition: under **50%** of the gap gets a cause, OR both users say they already have
  this number.

## Result

- Part 1 failed. Trader A 0%, Trader B 5.5%. Both under 50%, so B is wrong as written.
- Part 2 held. Both named a decision. Trader A: he'll check every leg's qty before adding real money.
  Trader B: he'll fix the futures price source first, and if the gap is real, change order type or
  entry logic.
- Neither user already had the number.

## Version C - after both users

What changed: I thought the hard part was finding the cause of the gap. It isn't. The hard part
comes before that - the paper side and the live side often can't be lined up at all (no per-leg
price for Trader A, no timestamps for Trader B, a missing hedge nobody spotted). Both users said this in
their own words; Trader B's line was "If comparison itself wrong then slippage number ka koi meaning
nahi hai."

**If every live fill is first matched to its paper row on instrument, planned qty and timestamp,
then in one session every short or missing leg gets flagged when it happens, and once timestamps
are there at least 80% of the Rs gap gets a named cause.**

- Kill condition: if the trader's data has timestamps and planned qty and I still can't give a
  cause to at least 50% of the gap, OR the next 2 traders I talk to say a leg mismatch has never
  happened to them. I won't move these lines untill I've run it on 2 more people.
