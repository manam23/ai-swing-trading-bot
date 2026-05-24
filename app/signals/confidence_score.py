def calculate_confidence_score(

    data,

    trend,

    signal,

    volume_breakout,

    candlestick_pattern
):

    latest = data.iloc[-1]


    ema20 = latest["EMA_20"]

    ema50 = latest["EMA_50"]

    ema200 = latest["EMA_200"]

    rsi = latest["RSI"]


    # HANDLE SERIES VALUES

    if hasattr(ema20, "iloc"):

        ema20 = ema20.iloc[0]

    if hasattr(ema50, "iloc"):

        ema50 = ema50.iloc[0]

    if hasattr(ema200, "iloc"):

        ema200 = ema200.iloc[0]

    if hasattr(rsi, "iloc"):

        rsi = rsi.iloc[0]


    ema20 = float(ema20)

    ema50 = float(ema50)

    ema200 = float(ema200)

    rsi = float(rsi)


    confidence = 50


    # EMA ALIGNMENT

    if ema20 > ema50 > ema200:

        confidence += 15

    elif ema20 < ema50 < ema200:

        confidence += 15


    # RSI STRENGTH

    if signal == "BUY":

        if rsi > 60:

            confidence += 10

    elif signal == "SELL":

        if rsi < 40:

            confidence += 10


    # VOLUME BREAKOUT

    if volume_breakout:

        confidence += 15


    # CANDLESTICK PATTERN

    bullish_patterns = [

        "HAMMER",

        "BULLISH"
    ]

    bearish_patterns = [

        "SHOOTING_STAR",

        "BEARISH"
    ]


    if (

        signal == "BUY"

        and

        candlestick_pattern in bullish_patterns
    ):

        confidence += 10


    if (

        signal == "SELL"

        and

        candlestick_pattern in bearish_patterns
    ):

        confidence += 10


    # TREND BONUS

    if trend == "BULLISH":

        confidence += 10

    elif trend == "BEARISH":

        confidence += 10


    return min(confidence, 100)