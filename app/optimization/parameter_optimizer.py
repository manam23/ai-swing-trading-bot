import pandas as pd

from app.scanner.data_fetcher import (
    fetch_stock_data
)


def calculate_custom_ema(

    data,

    short_ema,

    long_ema
):

    data["EMA_SHORT"] = (
        data["Close"]
        .ewm(span=short_ema)
        .mean()
    )

    data["EMA_LONG"] = (
        data["Close"]
        .ewm(span=long_ema)
        .mean()
    )

    return data


def calculate_custom_rsi(

    data,

    period=14
):

    delta = data["Close"].diff()

    gain = (
        delta.where(delta > 0, 0)
    ).rolling(period).mean()

    loss = (
        -delta.where(delta < 0, 0)
    ).rolling(period).mean()

    rs = gain / loss

    data["RSI"] = (
        100 - (100 / (1 + rs))
    )

    return data


def run_parameter_test(

    symbol,

    short_ema,

    long_ema,

    rsi_buy
):

    data = fetch_stock_data(

        symbol=symbol,

        interval="1d",

        period="2y"
    )

    if data is None or data.empty:

        return None


    # =========================
    # APPLY INDICATORS
    # =========================

    data = calculate_custom_ema(

        data,

        short_ema,

        long_ema
    )

    data = calculate_custom_rsi(data)


    total_trades = 0

    winning_trades = 0


    # =========================
    # MAIN BACKTEST LOOP
    # =========================

    for i in range(long_ema, len(data) - 5):

        current = data.iloc[i]

        future_data = data.iloc[i:i + 5]


        signal = "NO SIGNAL"


        # =========================
        # BUY CONDITION
        # =========================

        if (

            current["EMA_SHORT"]
            > current["EMA_LONG"]

            and

            current["RSI"] < rsi_buy
        ):

            signal = "BUY"


        if signal == "NO SIGNAL":

            continue


        entry = current["Close"]


        # =========================
        # REALISTIC TARGET
        # =========================

        target = entry * 1.02


        future_high = future_data[
            "High"
        ].max()


        total_trades += 1


        # =========================
        # WIN CHECK
        # =========================

        if future_high >= target:

            winning_trades += 1


    # =========================
    # FINAL WIN RATE
    # =========================

    if total_trades > 0:

        win_rate = round(

            (
                winning_trades
                / total_trades
            ) * 100,

            2
        )

    else:

        win_rate = 0


    return {

        "EMA": f"{short_ema}/{long_ema}",

        "RSI Buy": rsi_buy,

        "Trades": total_trades,

        "Wins": winning_trades,

        "Win Rate": win_rate
    }


def optimize_strategy(

    symbol="RELIANCE.NS"
):

    print(
        "\n========== AI PARAMETER OPTIMIZATION =========="
    )


    results = []


    short_ema_values = [10, 15, 20]

    long_ema_values = [30, 50, 100]

    rsi_values = [40, 50, 60]


    # =========================
    # PARAMETER TESTING
    # =========================

    for short_ema in short_ema_values:

        for long_ema in long_ema_values:

            if short_ema >= long_ema:

                continue


            for rsi_buy in rsi_values:

                try:

                    result = run_parameter_test(

                        symbol,

                        short_ema,

                        long_ema,

                        rsi_buy
                    )

                    if result:

                        results.append(result)

                        print(
                            f"EMA {short_ema}/{long_ema} | "
                            f"RSI {rsi_buy} | "
                            f"Trades: {result['Trades']} | "
                            f"Win Rate: "
                            f"{result['Win Rate']}%"
                        )

                except Exception as e:

                    print(
                        f"Error: {e}"
                    )


    results_df = pd.DataFrame(results)


    # =========================
    # SORT RESULTS
    # =========================

    ranked_df = results_df.sort_values(

        by=["Win Rate", "Trades"],

        ascending=False
    )


    print(
        "\n========== BEST PARAMETERS ==========\n"
    )

    print(ranked_df.head(10))


if __name__ == "__main__":

    optimize_strategy()