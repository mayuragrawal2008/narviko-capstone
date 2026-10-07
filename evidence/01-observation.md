# 1. Observation

Retail traders in India who run their own strategies on a broker API test them on paper first,
then decide how much real money to put on them. To make that call they need to know how far the
live result is from paper, and why. Nobody I spoke to had that number. Trader A has seen "differences
between the bot's expected trade and the actual execution" but couldn't put a rupee figure on
them. Trader B adjusts his limit price "by feel" for slippage he knows is there. When I compared
their paper and live positions by hand it broke in two places. First, the two sides often can't
even be lined up - Trader A's paper record was a single day total, not a price per leg, and Trader B's had
no timestamps, so a 130 point gap on a NIFTY future could not be told apart from slippage. Second,
positions drift and nobody sees it: Trader A's NIFTY position had 5 lots short but only 1 lot of hedge
on each side, and he told me "Honestly maine notice bhi nahi kiya tha. I was just checking overall
pnl in kite." I've had the same thing happen to me - on 26 Aug my own engine filled 3 of 4 legs of
a BANKNIFTY order and I only found out hours later from the logs.

## What each user confirmed or broke

| Claim | Trader A | Trader B |
|---|---|---|
| The paper-vs-live gap is not measured | Confirms. No Rs figure in the interview. When he saw Rs 22,884: "itna difference hai wo nahi pata tha" | Confirms. Absorbs slippage into the limit price by feel, no number |
| Position drift is found late, or never | Confirms. NIFTY long legs filled 1 of 5 lots, he hadn't noticed | Not tested - all his positions were single legs |
| The capital decision is a guess | Confirms, partly. Waiting for "consistent results" against his own benchmark before scaling | Breaks it a bit. His answer was about capital size and mindset, not about checking paper vs live |

My own numbers, for context: my engine has done 422 paper trades, Rs 4,93,482 net in 39 days, and
Rs 0 of that is live. I recieved the same kind of data from both users and neither of them could
answer "how much of this survives live" either.
