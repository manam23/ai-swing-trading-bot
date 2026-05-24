import sqlite3
import pandas as pd


DB_NAME = "trade_history.db"


def view_trade_signals():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM trade_signals
    ORDER BY timestamp DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


if __name__ == "__main__":

    df = view_trade_signals()

    print(df)