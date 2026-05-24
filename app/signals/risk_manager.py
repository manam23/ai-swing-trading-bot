def calculate_trade_levels(data, signal):

    latest = data.iloc[-1]

    close_price = latest["Close"]

    atr = latest["ATR"]


    # HANDLE SERIES VALUES

    if hasattr(close_price, "iloc"):

        close_price = close_price.iloc[0]

    if hasattr(atr, "iloc"):

        atr = atr.iloc[0]


    close_price = float(close_price)

    atr = float(atr)


    # BUY TRADE

    if signal == "BUY":

        entry = round(close_price, 2)

        stop_loss = round(
            close_price - (atr * 1.5),
            2
        )

        target = round(
            close_price + (atr * 3),
            2
        )


    # SELL TRADE

    elif signal == "SELL":

        entry = round(close_price, 2)

        stop_loss = round(
            close_price + (atr * 1.5),
            2
        )

        target = round(
            close_price - (atr * 3),
            2
        )


    else:

        return None


    return {

        "entry": entry,

        "sl": stop_loss,

        "target": target
    }