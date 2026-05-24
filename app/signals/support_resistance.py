def calculate_support_resistance(df):

    support = round(
        df["Low"].tail(20).min(),
        2
    )

    resistance = round(
        df["High"].tail(20).max(),
        2
    )

    return {
        "support": support,
        "resistance": resistance
    }