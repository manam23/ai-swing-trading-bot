import sqlite3


DB_NAME = "trade_history.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trade_signals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            stock TEXT,

            signal TEXT,

            trade_quality TEXT,

            confidence INTEGER,

            entry_price REAL,

            stop_loss REAL,

            target_price REAL,

            trend TEXT,

            daily_trend TEXT,

            breakout_signal TEXT,

            support REAL,

            resistance REAL,

            atr REAL,

            rsi REAL,

            trade_status TEXT DEFAULT 'OPEN',

            exit_price REAL DEFAULT 0,

            pnl REAL DEFAULT 0,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()

    conn.close()


def save_trade_signal(

    stock,
    signal,
    trade_quality,
    confidence,
    entry_price,
    stop_loss,
    target_price,
    trend,
    daily_trend,
    breakout_signal,
    support,
    resistance,
    atr,
    rsi
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO trade_signals (

            stock,
            signal,
            trade_quality,
            confidence,
            entry_price,
            stop_loss,
            target_price,
            trend,
            daily_trend,
            breakout_signal,
            support,
            resistance,
            atr,
            rsi

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            stock,
            signal,
            trade_quality,
            confidence,
            entry_price,
            stop_loss,
            target_price,
            trend,
            daily_trend,
            breakout_signal,
            support,
            resistance,
            atr,
            rsi
        )
    )

    conn.commit()

    conn.close()


if __name__ == "__main__":

    create_database()

    print("Database Created Successfully")