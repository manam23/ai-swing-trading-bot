import yfinance as yf

from app.indicators.rsi_indicator import (
    calculate_rsi
)

from app.indicators.ema_indicator import (
    calculate_ema
)

from app.signals.trend_detector import (
    detect_trend
)

from app.signals.buy_signal import (
    generate_buy_signal
)


def fetch_stock_data(

    symbol="RELIANCE.NS",

    interval="1h",

    period="3mo"
):

    try:

        print(f"\nFetching data for {symbol}...")

        df = yf.download(

            tickers=symbol,

            interval=interval,

            period=period,

            progress=False,

            threads=False,

            timeout=15
        )

        if df.empty:

            print(f"\nNo data found for {symbol}")

            return None

        df.dropna(inplace=True)

        return df

    except Exception as e:

        print(f"\nError fetching data for {symbol}: {e}")

        return None


if __name__ == "__main__":

    data = fetch_stock_data()

    if data is None:

        exit()

    data = calculate_ema(data)

    data = calculate_rsi(data)

    trend = detect_trend(data)

    signal = generate_buy_signal(
        data,
        trend
    )

    print(

        data[
            [
                "Close",
                "EMA_20",
                "EMA_50",
                "EMA_200",
                "RSI"
            ]
        ].tail()
    )

    print("\nMarket Trend:", trend)

    print("Trading Signal:", signal)