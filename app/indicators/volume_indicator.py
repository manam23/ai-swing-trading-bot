def calculate_volume_strength(data):

    latest = data.iloc[-1]

    current_volume = latest["Volume"]

    avg_volume = data["Volume"].tail(20).mean()


    # HANDLE SERIES VALUES

    if hasattr(current_volume, "iloc"):

        current_volume = current_volume.iloc[0]

    if hasattr(avg_volume, "iloc"):

        avg_volume = avg_volume.iloc[0]


    current_volume = float(current_volume)

    avg_volume = float(avg_volume)


    if avg_volume == 0:

        volume_ratio = 0

    else:

        volume_ratio = round(
            current_volume / avg_volume,
            2
        )


    volume_breakout = False


    if volume_ratio >= 1.5:

        volume_breakout = True


    return {

        "volume_ratio": volume_ratio,

        "volume_breakout": volume_breakout
    }