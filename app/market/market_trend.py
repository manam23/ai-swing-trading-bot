from app.scanner.data_fetcher import fetch_stock_data

from app.indicators.ema_indicator import calculate_ema

from app.signals.trend_detector import detect_trend


def get_nifty_trend():

    data = fetch_stock_data(
        symbol="^NSEI"
    )

    if data is None or data.empty:

        return "UNKNOWN"

    data = calculate_ema(data)

    trend = detect_trend(data)

    return trend