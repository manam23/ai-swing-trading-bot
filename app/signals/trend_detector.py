def detect_trend(data):

    latest = data.iloc[-1]


    ema20 = latest["EMA_20"]

    ema50 = latest["EMA_50"]

    ema200 = latest["EMA_200"]


    # HANDLE SERIES ISSUE
    if hasattr(ema20, "iloc"):

        ema20 = ema20.iloc[0]

    if hasattr(ema50, "iloc"):

        ema50 = ema50.iloc[0]

    if hasattr(ema200, "iloc"):

        ema200 = ema200.iloc[0]


    ema20 = float(ema20)

    ema50 = float(ema50)

    ema200 = float(ema200)


    if (

        ema20 > ema50

        and

        ema50 > ema200
    ):

        return "BULLISH"


    elif (

        ema20 < ema50

        and

        ema50 < ema200
    ):

        return "BEARISH"


    else:

        return "SIDEWAYS"