# Data retrieval and management

import yfinance as yf

def get_last_two_closes(symbol):
    df = yf.download(symbol, period="3d", interval="1d")
    return df['Close'].iloc[-2], df['Close'].iloc[-1]