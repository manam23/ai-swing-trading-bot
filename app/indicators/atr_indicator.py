import pandas as pd
def calculate_atr(df, period=14):

    high_low = df["High"] - df["Low"]

    high_close = abs(df["High"] - df["Close"].shift())

    low_close = abs(df["Low"] - df["Close"].shift())

    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    ).max(axis=1)

    atr = true_range.rolling(period).mean()

    df["ATR"] = atr

    return df