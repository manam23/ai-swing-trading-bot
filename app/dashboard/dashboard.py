import sys
import os

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

from streamlit_autorefresh import st_autorefresh

from app.scanner.data_fetcher import fetch_stock_data
from app.indicators.ema_indicator import calculate_ema
from app.database.performance_tracker import get_trade_performance


DB_NAME = "trade_history.db"


st.set_page_config(
    page_title="AI Swing Trading Dashboard",
    layout="wide"
)


# =========================
# AUTO REFRESH
# =========================

st_autorefresh(
    interval=15 * 1000,
    key="dashboard_refresh"
)


# =========================
# TITLE
# =========================

st.title("🚀 AI Swing Trading Dashboard")


# =========================
# LOAD DATABASE
# =========================

def load_trade_history():

    if not os.path.exists(DB_NAME):
        return pd.DataFrame()

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM trade_signals
    ORDER BY timestamp DESC
    """

    try:
        df = pd.read_sql_query(query, conn)

    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df


df = load_trade_history()


# =========================
# EMPTY DATABASE CHECK
# =========================

if df.empty:

    st.warning(
        "No trade data available yet."
    )

    st.stop()


performance = get_trade_performance()


# =========================
# PERFORMANCE METRICS
# =========================

total_signals = performance["total_trades"]

buy_signals = performance["buy_trades"]

sell_signals = performance["sell_trades"]

win_rate = performance["win_rate"]


open_trades = len(
    df[df["trade_status"] == "OPEN"]
)

winning_completed = len(
    df[df["trade_status"] == "WIN"]
)

losing_completed = len(
    df[df["trade_status"] == "LOSS"]
)

total_pnl = round(
    df["pnl"].sum(),
    2
)


col1, col2, col3, col4 = st.columns(4)

col5, col6, col7, col8 = st.columns(4)


col1.metric(
    "Total Signals",
    total_signals
)

col2.metric(
    "BUY Signals",
    buy_signals
)

col3.metric(
    "SELL Signals",
    sell_signals
)

col4.metric(
    "Win Rate",
    f"{win_rate}%"
)

col5.metric(
    "Winning Trades",
    winning_completed
)

col6.metric(
    "Losing Trades",
    losing_completed
)

col7.metric(
    "OPEN Trades",
    open_trades
)

col8.metric(
    "Total PnL",
    f"₹{total_pnl}"
)


st.divider()


# =========================
# FILTERS
# =========================

signal_filter = st.selectbox(
    "Filter By Signal",
    ["ALL", "BUY", "SELL"]
)

status_filter = st.selectbox(
    "Filter By Trade Status",
    ["ALL", "OPEN", "WIN", "LOSS"]
)


filtered_df = df.copy()


if signal_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["signal"] == signal_filter
    ]


if status_filter != "ALL":

    filtered_df = filtered_df[
        filtered_df["trade_status"] == status_filter
    ]


# =========================
# TABLE
# =========================

st.subheader("📊 Trade Signal History")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.divider()


# =========================
# STOCK CHART
# =========================

st.subheader("📈 Professional Trading Chart")


stock_list = filtered_df["stock"].unique()


if len(stock_list) > 0:

    selected_stock = st.selectbox(
        "Select Stock",
        stock_list
    )

    chart_data = fetch_stock_data(
        selected_stock
    )

    chart_data = calculate_ema(
        chart_data
    )

    fig = go.Figure()

    latest_trade = filtered_df[
        filtered_df["stock"] == selected_stock
    ].iloc[0]

    support = float(latest_trade["support"])

    resistance = float(latest_trade["resistance"])

    signal = latest_trade["signal"]

    trade_status = latest_trade["trade_status"]

    pnl = latest_trade["pnl"]

    fig.add_trace(

        go.Candlestick(

            x=chart_data.index,

            open=chart_data["Open"],

            high=chart_data["High"],

            low=chart_data["Low"],

            close=chart_data["Close"],

            name="Candlestick"
        )
    )

    fig.add_trace(

        go.Scatter(

            x=chart_data.index,

            y=chart_data["EMA_20"],

            mode="lines",

            name="EMA 20"
        )
    )

    fig.add_trace(

        go.Scatter(

            x=chart_data.index,

            y=chart_data["EMA_50"],

            mode="lines",

            name="EMA 50"
        )
    )

    fig.add_hline(
        y=support,
        line_dash="dot",
        annotation_text="Support"
    )

    fig.add_hline(
        y=resistance,
        line_dash="dot",
        annotation_text="Resistance"
    )

    latest_close = chart_data["Close"].iloc[-1]

    latest_date = chart_data.index[-1]

    marker_symbol = (
        "triangle-up"
        if signal == "BUY"
        else "triangle-down"
    )

    fig.add_trace(

        go.Scatter(

            x=[latest_date],

            y=[latest_close],

            mode="markers",

            marker=dict(
                size=16,
                symbol=marker_symbol
            ),

            name=f"{signal} Signal"
        )
    )

    fig.update_layout(

        title=(
            f"{selected_stock} | "
            f"Status: {trade_status} | "
            f"PnL: ₹{pnl}"
        ),

        height=750,

        xaxis_title="Date",

        yaxis_title="Price",

        template="plotly_dark",

        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "No trade signals available for chart display."
    )