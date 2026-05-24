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

# =========================
# LIVE AUTO REFRESH
# =========================

st.subheader("🔄 Live Market Dashboard")

refresh_interval = st.slider(

    "Auto Refresh Interval (Seconds)",

    min_value=5,

    max_value=60,

    value=15
)

st_autorefresh(

    interval=refresh_interval * 1000,

    key="live_dashboard_refresh"
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

        st.warning("Database file not found.")

        return pd.DataFrame()

    try:

        conn = sqlite3.connect(DB_NAME)

        query = """
        SELECT *
        FROM trade_signals
        ORDER BY id DESC
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    except Exception as e:

        st.error(f"Database Error: {e}")

        return pd.DataFrame()


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

# =========================
# STOCK CHART
# =========================

st.subheader("📈 Professional Trading Chart")

st.subheader("🔍 Search Any NSE Stock")

custom_stock = st.text_input(

    "Enter NSE Stock Symbol",

    placeholder="Example: IDEA, IRCTC, ZOMATO"
)

stock_list = filtered_df["stock"].unique()


if custom_stock:

    selected_stock = (
        f"{custom_stock.upper()}.NS"
    )

else:

    selected_stock = st.selectbox(

        "Select Stock",

        stock_list
    )


chart_data = fetch_stock_data(
    selected_stock
)

if chart_data is None or chart_data.empty:

    st.error(
        f"No market data found for {selected_stock}"
    )

    st.stop()

chart_data = calculate_ema(
    chart_data
)

fig = go.Figure()


stock_rows = filtered_df[
    filtered_df["stock"] == selected_stock
]


if len(stock_rows) > 0:

    latest_trade = stock_rows.iloc[0]

    support = float(latest_trade["support"])

    resistance = float(latest_trade["resistance"])

    signal = latest_trade["signal"]

    trade_status = latest_trade["trade_status"]

    pnl = latest_trade["pnl"]

else:

    support = float(chart_data["Low"].tail(20).min())

    resistance = float(chart_data["High"].tail(20).max())

    signal = "BUY"

    trade_status = "LIVE"

    pnl = 0


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


# =========================
# SUPPORT LINE
# =========================

# =========================
# SUPPORT LINE
# =========================

fig.add_shape(
    type="line",
    x0=chart_data.index[0],
    x1=chart_data.index[-1],
    y0=support,
    y1=support,
    line=dict(
        color="lime",
        width=2,
        dash="dot"
    )
)
# =========================
# RESISTANCE LINE
# =========================

fig.add_shape(
    type="line",
    x0=chart_data.index[0],
    x1=chart_data.index[-1],
    y0=resistance,
    y1=resistance,
    line=dict(
        color="red",
        width=2,
        dash="dot"
    )
)

fig.add_annotation(
    x=chart_data.index[-1],
    y=resistance,
    text=f"🔴 RESISTANCE ₹{round(resistance,2)}",
    showarrow=False,
    font=dict(color="red", size=14)
)


# =========================
# LATEST PRICE
# =========================

latest_close = chart_data["Close"].iloc[-1]

latest_date = chart_data.index[-1]
# =========================
# SIGNAL COLORS
# =========================

signal_color = (

    "lime"

    if signal == "BUY"

    else "red"
)

signal_symbol = (

    "triangle-up"

    if signal == "BUY"

    else "triangle-down"
)

# =========================
# BUY SELL LABEL
# =========================

fig.add_annotation(
    x=latest_date,
    y=latest_close,
    text=f"🟢 BUY" if signal == "BUY" else "🔴 SELL",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor=signal_color,
    ax=40,
    ay=-40,
    font=dict(
        color=signal_color,
        size=16
    )
)
# =========================
# SIGNAL COLORS
# =========================

signal_color = (

    "lime"

    if signal == "BUY"

    else "red"
)


signal_symbol = (

    "triangle-up"

    if signal == "BUY"

    else "triangle-down"
)


# =========================
# ENTRY LABEL
# =========================

entry_label = (

    f"{signal}<br>"
    f"Entry: ₹{round(latest_close,2)}<br>"
    f"Support: ₹{round(support,2)}<br>"
    f"Resistance: ₹{round(resistance,2)}"
)


# =========================
# BUY / SELL MARKER
# =========================

fig.add_trace(

    go.Scatter(

        x=[latest_date],

        y=[latest_close],

        mode="markers+text",

        marker=dict(

            size=36,

            color=signal_color,

            symbol=signal_symbol,

            line=dict(
                width=3,
                color="white"
            )
        ),

        text=[entry_label],

        textposition="top center",

        textfont=dict(
            size=14
        ),

        name=f"{signal} Signal"
    )
)


# =========================
# ENTRY PRICE LINE
# =========================

# =========================
# ENTRY PRICE LINE
# =========================

fig.add_shape(
    type="line",
    x0=chart_data.index[0],
    x1=chart_data.index[-1],
    y0=latest_close,
    y1=latest_close,
    line=dict(
        color=signal_color,
        width=2,
        dash="dash"
    )
)

fig.add_annotation(
    x=chart_data.index[-1],
    y=latest_close,
    text=f"{signal} ENTRY ₹{round(latest_close,2)}",
    showarrow=False,
    font=dict(color=signal_color, size=14)
)

fig.update_layout(

    title=(

        f"{selected_stock} | "

        f"Status: {trade_status} | "

        f"PnL: ₹{pnl}"
    ),

    height=900,

    xaxis_title="Date",

    yaxis_title="Price",

    template="plotly_dark",

    xaxis_rangeslider_visible=False
)


st.plotly_chart(

    fig,

    use_container_width=True
)