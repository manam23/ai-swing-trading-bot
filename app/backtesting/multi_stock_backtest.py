from app.backtesting.backtest_engine import (
    run_backtest
)

from app.config.settings import (
    NIFTY50_STOCKS
)


def run_multi_stock_backtest():

    print(
        "\n========== MULTI-STOCK BACKTEST =========="
    )

    for stock in NIFTY50_STOCKS:

        try:

            print("\n----------------------------------")

            run_backtest(stock)

        except Exception as e:

            print(
                f"\nError testing {stock}: {e}"
            )


if __name__ == "__main__":

    run_multi_stock_backtest()