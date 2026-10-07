# 6. Interview Notes

Both interviews were over WhatsApp text on 14 Sep. I sent the same 7 questions to both:

1. Are you running something live on Kite right now, or paper? Since when?
2. What did the backtest or paper say it would make? What did it make live? Do you have the
   number, or a feeling?
3. Tell me about the last time your bot's positions did not match what Kite showed. What happened,
   how did you find out, how long until you noticed?
4. Where are you at 9:15? What do you do if something goes wrong at 10:40 while you are busy?
5. How much is on it today? What would have to be true for you to put in 5x more?
6. Kite has the positions API and Console; OpenAlgo shows a P&L page; a scheduled script can diff
   them every few minutes. Does that already cover you? Why not?
7. Can you send me one session's tradebook and what your bot expected for the same trades? I will
   reconcile it by hand and send it back.

Their answers below are copied as they wrote them.

---

## Trader A

Questions at 12:57, answers at 13:09. About 12 minutes.

**How he does it today:** his bot runs in paper mode, no real money yet. He built a Telegram bot
that pings him when something happens, so he doesn't sit and watch the screen. He does see the bot's
expected price and the actual execution differ, and puts it down to volatility and order
restrictions. He doesn't keep a number for it.

| Q | Trader A's words |
|---|---|
| 1 | "Currently, I am doing paper trading and testing. I haven't started live trading with real money yet." |
| 2 | "So far, I have tested 7 trades, and 4 of them were profitable." |
| 3 | "Yes, I often see differences between the bot's expected trade and the actual execution conditions. This is mainly because of market volatility and order/execution restrictions." |
| 4 | "I have automated a Telegram bot to send me alerts. So, if something happens while I am busy, I can get notified instead of continuously monitoring the system." |
| 5 | "Since I am still in the testing stage, I want to see consistent results before putting in real money and scaling up. I would like the performance to meet my required benchmark consistently before increasing the capital significantly." |
| 6 | "I think there is still room for improvement. I would prefer a stable API along with an AI agent that can read the raw trading data, compare expected vs actual trades, and automatically identify differences." |
| 7 | "Yes, I can share one paper-trading session's trade data and what my bot expected, after removing any private/sensitive information." |

**What he actually sent:** not a tradebook. He first said no to sharing the full session, then
sent:

- A Sensibull positions snapshot, "Taken @ 30 Sep 2025, 3:40 PM" - 12 legs across NIFTY,
  BANKNIFTY and COFORGE options. Also typed out as `TraderA_Live.xlsx`.
- `TraderA_paper.xlsx` - a picture of a sheet, only columns J to P showing. It gives capital
  (Rs 38.14L), real P&L Rs 42,633 and paper P&L Rs 65,517 for the day.

What was missing: a paper price per leg (the columns with it are cut off), fill times, trade IDs.
The paper ROI is exactly the real ROI + 0.6 points, wich looks like a flat adjustment rather than
a trade by trade paper record. The xlsx also has the expiries as 2026 dates, the snapshot says 2025.

---

## Trader B

Questions at 14:28, answers at 14:31 and 14:35. About 7 minutes.

**How he does it today:** decides a trade from his rules plus news, fear:greed, MACD / RSI / EMA /
volume and gut feel. Before placing it he guesses how much the fill will be off, checks his
risk:reward still works, and sets the limit price from that. He knows the fill can be worse. He
doesn't write the difference down.

| Q | Trader B's words |
|---|---|
| 1 | "Not live. I trade manually. Started with paper trading in 2020 then started taking real trades manually on exchange." |
| 2 | "Trading is more about being emotionless and sticking to the rules we define for ourselves in maintaining the risk:reward ratio. News, FUD, fear:greed index, indicators like MACD RSI EMA VOL and most importantly gut feeling is what has worked in live trading for me" |
| 3 | "I havent tried bots. Even in manual trading I have observed that most exchanges open a market order when the limit order price is reached and then orders are filled. So some slippage or variance in buy price does happen. So I try to make sure to have that average buy price in mind with the variance which doesnt affect my risk:reward ratio and then I decide my limit order price." |
| 4 | "I usually wake up by 10:30am :) because I sleep late at night" |
| 5 | "More capital is required. It is easy to make 5% profit with large capital instead of making 500% profit with small capital. Mindset of a retailer is bound to loose money so think how the institutions trade and plan accordingly" |
| 6 | "Sounds interesting but never tried algo trading or high frequence trading" |
| 7 | Didn't answer in the chat, but sent the files later. |

Later that day he told me he does run an algo on paper money. That goes against his Q3 and Q6
answers. I took him at his word and didn't push. That message isn't in the screenshots here.

**What he actually sent:** `TraderB_Live.xlsx` and `TraderB_Paper.xlsx`. The same 15 open positions in
both (NIFTY futures and options, ABB, TRENT, UNITDSPR and VBL options), with the live entry price
in one and the paper entry price in the other.

What was missing: any date or time. The expiries go from Sep 2025 to Jun 2026, so these can't all
be from one day. The live sheet also had its P&L wrong on 3 rows (Rs 21 in total). No order type.

Things I didn't ask either of them and should have: which instruments they trade most, how much
capital they actually have on it, and how many minutes a day they spend checking.
