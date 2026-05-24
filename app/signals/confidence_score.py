def calculate_confidence_score(
    df,
    trend,
    signal,
    volume_breakout,
    candlestick_pattern
):

    latest = df.iloc[-1]

    score = 0

    rsi = latest["RSI"]

    ema20 = latest["EMA_20"]

    ema50 = latest["EMA_50"]

    ema200 = latest["EMA_200"]

    close = latest["Close"]


    # TREND STRENGTH

    if trend == "BULLISH":

        score += 30

    elif trend == "BEARISH":

        score += 30


    # EMA ALIGNMENT

    if ema20 > ema50 > ema200:

        score += 20

    elif ema20 < ema50 < ema200:

        score += 20


    # RSI QUALITY

    if signal == "BUY":

        if 55 <= rsi <= 70:

            score += 15

    elif signal == "SELL":

        if 30 <= rsi <= 45:

            score += 15


    # PRICE POSITION

    if signal == "BUY" and close > ema20:

        score += 15

    elif signal == "SELL" and close < ema20:

        score += 15


    # VOLUME CONFIRMATION

    if volume_breakout:

        score += 10


    # CANDLESTICK CONFIRMATION

    if candlestick_pattern in [
        "Bullish Engulfing",
        "Bearish Engulfing"
    ]:

        score += 10


    elif candlestick_pattern in [
        "Hammer",
        "Shooting Star"
    ]:

        score += 8


    elif candlestick_pattern == "Doji":

        score += 3


    return min(score, 100)