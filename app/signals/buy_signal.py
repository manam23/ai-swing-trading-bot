def generate_buy_signal(df, trend):

    latest = df.iloc[-1]

    rsi = latest["RSI"]

    if trend == "BULLISH" and rsi > 55:

        return "BUY"

    elif trend == "BEARISH" and rsi < 40:

        return "SELL"

    else:

        return "NO SIGNAL"