# Live trading execution

from data import get_last_two_closes
from strategy import calculate_buy_amount
from risk import apply_risk
from broker import place_etf_order
import datetime

red_streak = 0
monthly_used = 0

prev_close, today_close = get_last_two_closes("^NSEI")
daily_return = (today_close - prev_close) / prev_close

if daily_return < 0:
    red_streak += 1
else:
    red_streak = 0

raw_buy = calculate_buy_amount(daily_return, red_streak)
final_buy = apply_risk(raw_buy, 0, monthly_used)

if final_buy > 0:
    place_etf_order("NIFTYBEES", final_buy, today_close)
    monthly_used += final_buy