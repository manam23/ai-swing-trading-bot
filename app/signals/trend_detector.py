def detect_trend(df):

    latest = df.iloc[-1]

    if (
        latest["EMA_20"] >
        latest["EMA_50"] >
        latest["EMA_200"]
    ):

        return "BULLISH"

    elif (
        latest["EMA_20"] <
        latest["EMA_50"] <
        latest["EMA_200"]
    ):

        return "BEARISH"

    else:

        return "SIDEWAYS"