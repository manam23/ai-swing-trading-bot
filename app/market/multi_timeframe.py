from app.scanner.data_fetcher import fetch_stock_data

from app.indicators.ema_indicator import calculate_ema

from app.signals.trend_detector import detect_trend


def get_higher_timeframe_trend(symbol):

    data = fetch_stock_data(
        symbol=symbol,
        interval="1d",
        period="6mo"
    )

    if data is None or data.empty:

        return "UNKNOWN"

    data = calculate_ema(data)

    trend = detect_trend(data)

    return trend