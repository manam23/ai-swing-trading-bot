import pandas as pd

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


def run_backtest(

    symbol="RELIANCE.NS"
):

    print(f"\nRunning Backtest for {symbol}")


    # =========================
    # FETCH DATA
    # =========================

    data = fetch_stock_data(

        symbol=symbol,

        interval="1d",

        period="6mo"
    )


    if data is None or data.empty:

        print("No data found")

        return


    # =========================
    # APPLY INDICATORS
    # =========================

    data = calculate_ema(data)

    data = calculate_rsi(data)


    total_trades = 0

    winning_trades = 0

    losing_trades = 0

    total_pnl = 0


    # =========================
    # LOOP THROUGH DATA
    # =========================

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

            elif future_low <= stop_loss:

                trade_result = "LOSS"

                pnl = round(
                    stop_loss - entry,
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

            elif future_high >= stop_loss:

                trade_result = "LOSS"

                pnl = round(
                    entry - stop_loss,
                    2
                )


        total_trades += 1

        total_pnl += pnl


        if trade_result == "WIN":

            winning_trades += 1

        else:

            losing_trades += 1


    # =========================
    # FINAL RESULTS
    # =========================

    if total_trades > 0:

        win_rate = round(

            (winning_trades / total_trades) * 100,

            2
        )

    else:

        win_rate = 0


    print("\n========== BACKTEST RESULTS ==========")

    print(f"Stock: {symbol}")

    print(f"Total Trades: {total_trades}")

    print(f"Winning Trades: {winning_trades}")

    print(f"Losing Trades: {losing_trades}")

    print(f"Win Rate: {win_rate}%")

    print(f"Total PnL: ₹{round(total_pnl, 2)}")


if __name__ == "__main__":

    run_backtest()