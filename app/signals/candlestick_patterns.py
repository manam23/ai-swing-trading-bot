def detect_candlestick_pattern(data):

    latest = data.iloc[-1]


    open_price = latest["Open"]

    high_price = latest["High"]

    low_price = latest["Low"]

    close_price = latest["Close"]


    # HANDLE SERIES VALUES

    if hasattr(open_price, "iloc"):

        open_price = open_price.iloc[0]

    if hasattr(high_price, "iloc"):

        high_price = high_price.iloc[0]

    if hasattr(low_price, "iloc"):

        low_price = low_price.iloc[0]

    if hasattr(close_price, "iloc"):

        close_price = close_price.iloc[0]


    open_price = float(open_price)

    high_price = float(high_price)

    low_price = float(low_price)

    close_price = float(close_price)


    body = abs(close_price - open_price)

    candle_range = high_price - low_price


    upper_wick = high_price - max(
        open_price,
        close_price
    )

    lower_wick = min(
        open_price,
        close_price
    ) - low_price


    # HAMMER

    if (

        lower_wick > body * 2

        and

        upper_wick < body
    ):

        return "HAMMER"


    # SHOOTING STAR

    elif (

        upper_wick > body * 2

        and

        lower_wick < body
    ):

        return "SHOOTING_STAR"


    # BULLISH CANDLE

    elif close_price > open_price:

        return "BULLISH"


    # BEARISH CANDLE

    elif close_price < open_price:

        return "BEARISH"


    else:

        return "NEUTRAL"