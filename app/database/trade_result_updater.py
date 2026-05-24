import sqlite3
import pandas as pd
import yfinance as yf


DB_NAME = "trade_history.db"


def update_trade_results():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM trade_signals
    WHERE trade_status = 'OPEN'
    """

    df = pd.read_sql_query(query, conn)


    # =========================
    # NO OPEN TRADES
    # =========================

    if df.empty:

        print("\nNo OPEN trades found")

        conn.close()

        return


    # =========================
    # PROCESS EACH TRADE
    # =========================

    for _, trade in df.iterrows():

        stock = trade["stock"]

        signal = trade["signal"]

        target = trade["target_price"]

        stop_loss = trade["stop_loss"]

        entry = trade["entry_price"]

        trade_id = trade["id"]


        # =========================
        # FETCH LATEST PRICE
        # =========================

        latest_data = yf.Ticker(stock).history(
            period="1d"
        )

        if latest_data.empty:

            print(
                f"{stock} → "
                f"No latest market data"
            )

            continue


        latest_close = round(

            latest_data["Close"].iloc[-1],

            2
        )


        trade_status = "OPEN"

        pnl = 0


        # =========================
        # BUY LOGIC
        # =========================

        if signal == "BUY":

            if latest_close >= target:

                trade_status = "WIN"

                pnl = round(
                    target - entry,
                    2
                )

            elif latest_close <= stop_loss:

                trade_status = "LOSS"

                pnl = round(
                    stop_loss - entry,
                    2
                )


        # =========================
        # SELL LOGIC
        # =========================

        elif signal == "SELL":

            if latest_close <= target:

                trade_status = "WIN"

                pnl = round(
                    entry - target,
                    2
                )

            elif latest_close >= stop_loss:

                trade_status = "LOSS"

                pnl = round(
                    entry - stop_loss,
                    2
                )


        # =========================
        # LOG CURRENT STATUS
        # =========================

        print(
            f"{stock} | "
            f"Latest: {latest_close} | "
            f"Target: {target} | "
            f"SL: {stop_loss} | "
            f"Status: {trade_status}"
        )


        # =========================
        # UPDATE DATABASE
        # =========================

        if trade_status != "OPEN":

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE trade_signals

                SET trade_status = ?,
                    exit_price = ?,
                    pnl = ?

                WHERE id = ?
                """,
                (
                    trade_status,
                    latest_close,
                    pnl,
                    trade_id
                )
            )

            conn.commit()

            print(
                f"{stock} updated → "
                f"{trade_status} | "
                f"PnL: {pnl}"
            )


    conn.close()

    print("\nTrade result update completed")


if __name__ == "__main__":

    update_trade_results()