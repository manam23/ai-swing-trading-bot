def calculate_trade_levels(df, signal):

    latest = df.iloc[-1]

    entry_price = round(latest["Close"], 2)

    atr = latest["ATR"]

    if signal == "BUY":

        stop_loss = round(
            entry_price - (1.5 * atr),
            2
        )

        target = round(
            entry_price + (3 * atr),
            2
        )

    elif signal == "SELL":

        stop_loss = round(
            entry_price + (1.5 * atr),
            2
        )

        target = round(
            entry_price - (3 * atr),
            2
        )

    else:

        return None

    return {
        "entry": entry_price,
        "sl": stop_loss,
        "target": target
    }