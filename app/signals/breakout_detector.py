def detect_breakout(
    df,
    support,
    resistance,
    volume_breakout
):

    latest = df.iloc[-1]

    close_price = latest["Close"]


    # BULLISH BREAKOUT

    if (
        close_price > resistance
        and volume_breakout
    ):

        return "BULLISH BREAKOUT"


    # BEARISH BREAKDOWN

    if (
        close_price < support
        and volume_breakout
    ):

        return "BEARISH BREAKDOWN"


    return "NO BREAKOUT"