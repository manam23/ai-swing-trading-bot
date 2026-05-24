def calculate_volume_strength(df):

    latest = df.iloc[-1]

    current_volume = latest["Volume"]

    avg_volume = df["Volume"].tail(20).mean()

    volume_ratio = current_volume / avg_volume

    if volume_ratio >= 1.5:

        return {
            "volume_breakout": True,
            "volume_ratio": round(volume_ratio, 2)
        }

    return {
        "volume_breakout": False,
        "volume_ratio": round(volume_ratio, 2)
    }