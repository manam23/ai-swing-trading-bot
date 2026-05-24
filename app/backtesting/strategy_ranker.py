import pandas as pd

from app.config.settings import (
    NIFTY50_STOCKS
)

from app.scanner.data_fetcher import (
    fetch_stock_data
)

from app.indicators.ema_indicator import (
    calculate_ema
)

from app.indicators.rsi_indicator import (
    calculate_rsi
)

from app.signals.trend_detector import (
    detect_trend
)

from app.signals.buy_signal import (
    generate_buy_signal
)


def backtest_stock(symbol):

    data = fetch_stock_data(

        symbol=symbol,

        interval="1d",

        period="6mo"
    )

    if data is None or data.empty:

        return None


    data = calculate_ema(data)

    data = calculate_rsi(data)


    total_trades = 0

    winning_trades = 0

    total_pnl = 0


    for i in range(50, len(data) - 5):

        historical_data = data.iloc[:i]

        trend = detect_trend(
            historical_data
        )

        signal = generate_buy_signal(
            historical_data,
            trend
        )


        if signal == "NO SIGNAL":

            continue


        entry = historical_data[
            "Close"
        ].iloc[-1]


        future_data = data.iloc[i:i + 5]

        future_high = future_data[
            "High"
        ].max()

        future_low = future_data[
            "Low"
        ].min()


        trade_result = "LOSS"

        pnl = 0


        # =========================
        # BUY LOGIC
        # =========================

        if signal == "BUY":

            target = entry * 1.03

            stop_loss = entry * 0.98


            if future_high >= target:

                trade_result = "WIN"

                pnl = round(
                    target - entry,
                    2
                )


        # =========================
        # SELL LOGIC
        # =========================

        elif signal == "SELL":

            target = entry * 0.97

            stop_loss = entry * 1.02


            if future_low <= target:

                trade_result = "WIN"

                pnl = round(
                    entry - target,
                    2
                )


        total_trades += 1

        total_pnl += pnl


        if trade_result == "WIN":

            winning_trades += 1


    if total_trades > 0:

        win_rate = round(

            (winning_trades / total_trades) * 100,

            2
        )

    else:

        win_rate = 0


    return {

        "Stock": symbol,

        "Trades": total_trades,

        "Wins": winning_trades,

        "Win Rate": win_rate,

        "PnL": round(total_pnl, 2)
    }


def rank_strategies():

    results = []


    print(
        "\n========== STRATEGY RANKING =========="
    )


    for stock in NIFTY50_STOCKS:

        try:

            result = backtest_stock(stock)

            if result:

                results.append(result)

                print(
                    f"{stock} | "
                    f"Win Rate: {result['Win Rate']}% | "
                    f"PnL: ₹{result['PnL']}"
                )

        except Exception as e:

            print(
                f"Error testing {stock}: {e}"
            )


    results_df = pd.DataFrame(results)


    # =========================
    # SORT BY WIN RATE
    # =========================

    ranked_df = results_df.sort_values(

        by=["Win Rate", "PnL"],

        ascending=False
    )


    print(
        "\n========== TOP STRATEGY STOCKS ==========\n"
    )

    print(ranked_df.head(10))


if __name__ == "__main__":

    rank_strategies()