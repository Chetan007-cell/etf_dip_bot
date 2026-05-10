import yfinance as yf
from datetime import datetime

# ---------------- CONFIG ----------------
START_DATE = "2014-01-01"
INDEX_SYMBOL = "^NSEI"

BASE_UNIT = 1000
DEPTH_STEP = 0.0025  # 0.25%

MAX_DAILY_BUY = 10000
MAX_MONTHLY_BUY = 50000
# ----------------------------------------


def calculate_buy_amount(daily_return, red_streak):
    if daily_return >= 0:
        return 0

    depth_units = int(abs(daily_return) // DEPTH_STEP)
    streak_units = min(red_streak, 5)  # cap streak risk

    return (depth_units + streak_units) * BASE_UNIT


def apply_risk(buy_amount, monthly_used):
    if monthly_used >= MAX_MONTHLY_BUY:
        return 0

    return min(buy_amount, MAX_DAILY_BUY, MAX_MONTHLY_BUY - monthly_used)


# -------- LOAD DATA --------
data = yf.download(INDEX_SYMBOL, start=START_DATE, progress=True)

# -------- BACKTEST STATE --------
red_streak = 0
monthly_used = 0

units = 0.0
capital = 0.0

prev_month = None

# -------- BACKTEST LOOP --------
for i in range(1, len(data)):
    date = data.index[i]
    curr_month = date.month

    if prev_month is not None and curr_month != prev_month:
        monthly_used = 0  # reset monthly cap

    prev_close = float(data['Close'].iloc[i - 1])
    curr_close = float(data['Close'].iloc[i])

    daily_return = (curr_close - prev_close) / prev_close

    if daily_return < 0:
        red_streak += 1
    else:
        red_streak = 0

    raw_buy = calculate_buy_amount(daily_return, red_streak)
    final_buy = apply_risk(raw_buy, monthly_used)

    if final_buy > 0:
        units += final_buy / curr_close
        capital += final_buy
        monthly_used += final_buy

    prev_month = curr_month

# -------- RESULTS --------
final_value = units * float(data['Close'].iloc[-1])
returns_pct = (final_value / capital - 1) * 100 if capital > 0 else 0

print("\n===== BACKTEST RESULTS =====")
print(f"Capital Invested : ₹{capital:,.0f}")
print(f"Final Value     : ₹{final_value:,.0f}")
print(f"Return %        : {returns_pct:.2f}%")


