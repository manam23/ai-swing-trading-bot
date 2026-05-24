def generate_buy_signal(data, trend):

    latest = data.iloc[-1]


    ema20 = latest["EMA_20"]

    ema50 = latest["EMA_50"]

    rsi = latest["RSI"]


    # HANDLE SERIES VALUES
    if hasattr(ema20, "iloc"):

        ema20 = ema20.iloc[0]

    if hasattr(ema50, "iloc"):

        ema50 = ema50.iloc[0]

    if hasattr(rsi, "iloc"):

        rsi = rsi.iloc[0]


    ema20 = float(ema20)

    ema50 = float(ema50)

    rsi = float(rsi)


    # BUY SIGNAL
    if (

        trend == "BULLISH"

        and

        ema20 > ema50

        and

        rsi > 55
    ):

        return "BUY"


    # SELL SIGNAL
    elif (

        trend == "BEARISH"

        and

        ema20 < ema50

        and

        rsi < 45
    ):

        return "SELL"


    else:

        return "NO SIGNAL"