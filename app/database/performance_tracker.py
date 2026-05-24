import sqlite3
import pandas as pd


DB_NAME = "trade_history.db"


def get_trade_performance():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM trade_signals
    """

    df = pd.read_sql_query(query, conn)

    conn.close()


    # =========================
    # BASIC METRICS
    # =========================

    total_trades = len(df)

    buy_trades = len(
        df[df["signal"] == "BUY"]
    )

    sell_trades = len(
        df[df["signal"] == "SELL"]
    )


    # =========================
    # TEMPORARY WIN LOGIC
    # =========================

    # HIGH confidence = win
    # LOW confidence = loss

    winning_trades = len(
        df[df["confidence"] >= 80]
    )

    losing_trades = (
        total_trades - winning_trades
    )


    # =========================
    # WIN RATE
    # =========================

    if total_trades > 0:

        win_rate = round(

            (winning_trades / total_trades) * 100,

            2
        )

    else:

        win_rate = 0


    return {

        "total_trades": total_trades,

        "buy_trades": buy_trades,

        "sell_trades": sell_trades,

        "winning_trades": winning_trades,

        "losing_trades": losing_trades,

        "win_rate": win_rate
    }


if __name__ == "__main__":

    performance = get_trade_performance()

    print(performance)