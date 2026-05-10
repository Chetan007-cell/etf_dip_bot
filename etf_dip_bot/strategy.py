# Trading strategy logic
import math
from config import BASE_UNIT, DEPTH_STEP

def calculate_buy_amount(daily_return, red_streak):
    if daily_return >= 0:
        return 0

    depth_units = int(abs(daily_return) // DEPTH_STEP)
    streak_units = red_streak

    return (depth_units + streak_units) * BASE_UNIT


def my_formula_exponential(daily_return, red_streak):
    if daily_return >= 0:
        return 0

    fall = abs(daily_return)

    return math.exp(fall * 100) * (1 + red_streak) * 1000