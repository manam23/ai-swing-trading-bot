import schedule
import time

from app.scanner.data_fetcher import fetch_stock_data

from app.indicators.ema_indicator import calculate_ema
from app.indicators.rsi_indicator import calculate_rsi
from app.indicators.volume_indicator import calculate_volume_strength
from app.indicators.atr_indicator import calculate_atr

from app.signals.trend_detector import detect_trend
from app.signals.buy_signal import generate_buy_signal
from app.signals.risk_manager import calculate_trade_levels
from app.signals.confidence_score import calculate_confidence_score
from app.signals.candlestick_patterns import detect_candlestick_pattern

from app.signals.support_resistance import (
    calculate_support_resistance
)

from app.signals.breakout_detector import (
    detect_breakout
)

from app.signals.trade_quality import (
    get_trade_quality
)

from app.alerts.telegram_alert import send_telegram_alert

from app.market.market_trend import get_nifty_trend

from app.market.multi_timeframe import (
    get_higher_timeframe_trend
)

from app.database.db_manager import (
    save_trade_signal
)

from app.config.settings import NIFTY50_STOCKS
from app.utils.signal_memory import signal_cache


def scan_stock(symbol, nifty_trend):

    print(f"\nScanning {symbol}...")

    data = fetch_stock_data(symbol=symbol)

    if data is None or data.empty:

        print(f"No data found for {symbol}")

        return

    data = calculate_ema(data)

    data = calculate_rsi(data)

    data = calculate_atr(data)

    trend = detect_trend(data)

    higher_timeframe_trend = (
        get_higher_timeframe_trend(symbol)
    )

    signal = generate_buy_signal(data, trend)

    if signal == "NO SIGNAL":

        return

    # MULTI-TIMEFRAME FILTER

    if signal == "BUY":

        if higher_timeframe_trend != "BULLISH":

            print(
                f"{symbol} skipped due to bearish daily trend"
            )

            return

    if signal == "SELL":

        if higher_timeframe_trend != "BEARISH":

            print(
                f"{symbol} skipped due to bullish daily trend"
            )

            return

    # NIFTY MARKET FILTER

    if signal == "BUY" and nifty_trend != "BULLISH":

        print(f"{symbol} skipped due to bearish market")

        return

    if signal == "SELL" and nifty_trend != "BEARISH":

        print(f"{symbol} skipped due to bullish market")

        return

    trade_levels = calculate_trade_levels(data, signal)

    if trade_levels is None:

        return

    volume_data = calculate_volume_strength(data)

    volume_breakout = volume_data["volume_breakout"]

    volume_ratio = volume_data["volume_ratio"]

    candlestick_pattern = detect_candlestick_pattern(data)

    sr_levels = calculate_support_resistance(data)

    support = sr_levels["support"]

    resistance = sr_levels["resistance"]

    breakout_signal = detect_breakout(
        data,
        support,
        resistance,
        volume_breakout
    )

    confidence = calculate_confidence_score(
        data,
        trend,
        signal,
        volume_breakout,
        candlestick_pattern
    )

    trade_quality = get_trade_quality(
        confidence
    )

    if confidence < 70:

        print(f"{symbol} skipped due to low confidence")

        return

    previous_signal = signal_cache.get(symbol)

    if previous_signal == signal:

        print(f"{symbol} alert already sent")

        return

    signal_cache[symbol] = signal

    latest = data.iloc[-1]

    rsi_value = round(latest["RSI"], 2)

    ema20 = round(latest["EMA_20"], 2)

    ema50 = round(latest["EMA_50"], 2)

    atr_value = round(latest["ATR"], 2)

    entry_price = trade_levels["entry"]

    stop_loss = trade_levels["sl"]

    target_price = trade_levels["target"]

    print(
        f"{symbol} → {signal} | "
        f"Quality: {trade_quality} | "
        f"Breakout: {breakout_signal} | "
        f"Daily Trend: {higher_timeframe_trend} | "
        f"Support: {support} | "
        f"Resistance: {resistance} | "
        f"ATR: {atr_value} | "
        f"Pattern: {candlestick_pattern} | "
        f"Volume Breakout: {volume_breakout} | "
        f"Volume Ratio: {volume_ratio}"
    )

    message = f"""
🚨 SWING TRADE ALERT 🚨

Stock: {symbol}

Signal: {signal}

Trade Quality: {trade_quality}

Confidence: {confidence}%

NIFTY Trend: {nifty_trend}

Daily Trend: {higher_timeframe_trend}

Breakout Signal: {breakout_signal}

Support: ₹{support}

Resistance: ₹{resistance}

ATR: {atr_value}

Pattern: {candlestick_pattern}

Volume Breakout: {volume_breakout}

Volume Ratio: {volume_ratio}

Entry: ₹{entry_price}

Stop Loss: ₹{stop_loss}

Target: ₹{target_price}

Trend: {trend}

RSI: {rsi_value}

EMA20: {ema20}

EMA50: {ema50}
"""

    print(message)

    send_telegram_alert(message)

    # SAVE SIGNAL TO DATABASE

    save_trade_signal(

        stock=symbol,

        signal=signal,

        trade_quality=trade_quality,

        confidence=confidence,

        entry_price=entry_price,

        stop_loss=stop_loss,

        target_price=target_price,

        trend=trend,

        daily_trend=higher_timeframe_trend,

        breakout_signal=breakout_signal,

        support=support,

        resistance=resistance,

        atr=atr_value,

        rsi=rsi_value
    )


def run_market_scanner():

    nifty_trend = get_nifty_trend()

    print(f"\nNIFTY Trend: {nifty_trend}")

    print("\n==============================")
    print("Running Market Scanner...")
    print("==============================")

    for stock in NIFTY50_STOCKS:

        scan_stock(stock, nifty_trend)


if __name__ == "__main__":

    schedule.every(15).minutes.do(run_market_scanner)

    print("\n🚀 AI Swing Trading Bot Started...\n")

    run_market_scanner()

    while True:

        schedule.run_pending()

        time.sleep(1)