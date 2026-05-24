def detect_candlestick_pattern(df):

    latest = df.iloc[-1]

    previous = df.iloc[-2]


    latest_open = latest["Open"]

    latest_close = latest["Close"]

    latest_high = latest["High"]

    latest_low = latest["Low"]


    previous_open = previous["Open"]

    previous_close = previous["Close"]


    body = abs(latest_close - latest_open)

    candle_range = latest_high - latest_low

    lower_wick = min(
        latest_open,
        latest_close
    ) - latest_low

    upper_wick = latest_high - max(
        latest_open,
        latest_close
    )


    # BULLISH ENGULFING

    if (
        previous_close < previous_open
        and latest_close > latest_open
        and latest_open < previous_close
        and latest_close > previous_open
    ):

        return "Bullish Engulfing"


    # BEARISH ENGULFING

    if (
        previous_close > previous_open
        and latest_close < latest_open
        and latest_open > previous_close
        and latest_close < previous_open
    ):

        return "Bearish Engulfing"


    # HAMMER

    if (
        lower_wick > (2 * body)
        and upper_wick < body
    ):

        return "Hammer"


    # SHOOTING STAR

    if (
        upper_wick > (2 * body)
        and lower_wick < body
    ):

        return "Shooting Star"


    # DOJI

    if body < (0.1 * candle_range):

        return "Doji"


    return "No Pattern"