def calculate_support_resistance(data):

    recent_data = data.tail(20)


    support = recent_data["Low"].min()

    resistance = recent_data["High"].max()


    # HANDLE SERIES VALUES

    if hasattr(support, "iloc"):

        support = support.iloc[0]

    if hasattr(resistance, "iloc"):

        resistance = resistance.iloc[0]


    support = round(float(support), 2)

    resistance = round(float(resistance), 2)


    return {

        "support": support,

        "resistance": resistance
    }