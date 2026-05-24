import pandas as pd


def calculate_ema(df, periods=[20, 50, 200]):

    for period in periods:

        ema_column = f"EMA_{period}"

        df[ema_column] = df["Close"].ewm(
            span=period,
            adjust=False
        ).mean()

    return df