from app.backtesting.strategy_ranker import (
    backtest_stock
)

from app.config.settings import (
    NIFTY50_STOCKS
)


def simulate_portfolio(

    starting_capital=100000,

    risk_per_trade=0.02
):

    capital = starting_capital

    print(
        "\n========== PORTFOLIO SIMULATION =========="
    )

    print(f"\nStarting Capital: ₹{capital}")


    for stock in NIFTY50_STOCKS:

        try:

            result = backtest_stock(stock)

            if result is None:

                continue


            pnl = result["PnL"]

            trade_risk = capital * risk_per_trade


            # =========================
            # APPLY POSITION SCALING
            # =========================

            scaled_pnl = round(

                (pnl / 100) * trade_risk,

                2
            )


            capital += scaled_pnl


            print(
                f"\n{stock} | "
                f"PnL: ₹{scaled_pnl} | "
                f"Updated Capital: ₹{round(capital, 2)}"
            )


        except Exception as e:

            print(
                f"\nError processing {stock}: {e}"
            )


    total_return = round(

        (
            (capital - starting_capital)
            / starting_capital
        ) * 100,

        2
    )


    print(
        "\n========== FINAL PORTFOLIO RESULTS =========="
    )

    print(f"\nFinal Capital: ₹{round(capital, 2)}")

    print(f"Total Return: {total_return}%")

    print(
        f"Net Profit: ₹{round(capital - starting_capital, 2)}"
    )


if __name__ == "__main__":

    simulate_portfolio()