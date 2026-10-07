# 10. Bottleneck

**Step 5 - matching each live fill to its paper row on the same instrument, qty and time - failed
on 12 of 12 of Trader A's legs and ran with no timestamps on 15 of 15 of Trader B's rows, so every number
after it (slippage, cause, attributed %) sat on a comparison I couldn't check.**

## Why this step

- **Trader A:** his paper side had no price per leg, only a picture of a summary. Nothing to match
  against, so 0% of the Rs 22,884 gap got a cause. His planned lots weren't in the data either,
  which is why the 5 vs 1 partial fill got caught by eye in step 7 and not by a rule.
- **Trader B:** all 15 rows matched on symbol and qty, but with no times. So in step 8 I couldn't
  tell whether a 130 point futures gap was slippage or a different reference price. That one call
  moved his result between 5.5% and 100%.
- **Both of them said it without me asking:**
  - Trader B, 16:11: "Before changing limit/market order etc I need to know paper and live same
    instrument and same timestamp compare bhi kar rahe hai ya nahi. If comparison itself wrong
    then slippage number ka koi meaning nahi hai."
  - Trader A, 16:28: "Real money increase karne se pehle definitely ye check karunga ki all legs
    expected qty se match kar rahe hai."

Step 8 looked like the hard part while I was doing it, but it only went wrong because step 5 had
nothing to work with. Fix 5 and most of 8 becomes a rule.

## What I build first

For every live fill, find the paper row with the same instrument, the same planned qty and a time
inside a small window. Flag any leg with no match, or a qty short - like Trader A's missing 4 lots -
the moment it happens. Only rows that pass get a slippage number. Narviko already has the order
book, positions and paper P&L; this matching is the part it doesn't have.
