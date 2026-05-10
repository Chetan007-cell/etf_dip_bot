# Risk management and position sizing

from config import MAX_DAILY_BUY, MAX_MONTHLY_BUY

def apply_risk(buy_amount, daily_used, monthly_used):
    if monthly_used >= MAX_MONTHLY_BUY:
        return 0

    allowed = min(
        buy_amount,
        MAX_DAILY_BUY - daily_used,
        MAX_MONTHLY_BUY - monthly_used
    )

    return max(0, allowed)