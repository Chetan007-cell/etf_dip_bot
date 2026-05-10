from kiteconnect import KiteConnect

kite = KiteConnect(api_key="YOUR_API_KEY")

def place_etf_order(symbol, amount, price):
    quantity = amount // price
    if quantity == 0:
        return

    kite.place_order(
        tradingsymbol=symbol,
        exchange="NSE",
        transaction_type="BUY",
        quantity=quantity,
        order_type="MARKET",
        product="CNC"
    )