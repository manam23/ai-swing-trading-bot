def detect_breakout(

    data,

    support,

    resistance,

    volume_breakout
):

    latest = data.iloc[-1]

    close_price = latest["Close"]


    # HANDLE SERIES VALUES

    if hasattr(close_price, "iloc"):

        close_price = close_price.iloc[0]

    if hasattr(support, "iloc"):

        support = support.iloc[0]

    if hasattr(resistance, "iloc"):

        resistance = resistance.iloc[0]


    close_price = float(close_price)

    support = float(support)

    resistance = float(resistance)


    # BULLISH BREAKOUT

    if (

        close_price > resistance

        and

        volume_breakout
    ):

        return "BULLISH BREAKOUT"


    # BEARISH BREAKDOWN

    elif (

        close_price < support

        and

        volume_breakout
    ):

        return "BEARISH BREAKDOWN"


    else:

        return "NO BREAKOUT"