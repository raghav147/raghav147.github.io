"""Generate visualization of INO stock with key technical indicators."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "assets" / "image" / "ino_three_months_indicators.png"
TICKER = "INO"
PERIOD = "3mo"
INTERVAL = "1d"


@dataclass
class IndicatorSummary:
    latest_close: float
    sma20: float
    sma50: float
    rsi: float
    macd: float
    signal: float

    @property
    def trend(self) -> str:
        if self.sma20 > self.sma50:
            return "Short-term momentum is above the intermediate trend (20-day SMA above 50-day SMA)."
        if self.sma20 < self.sma50:
            return "Short-term momentum is below the intermediate trend (20-day SMA below 50-day SMA)."
        return "Short-term and intermediate trends are aligned."

    @property
    def rsi_comment(self) -> str:
        if self.rsi >= 70:
            return "RSI is in overbought territory (>70)."
        if self.rsi <= 30:
            return "RSI is in oversold territory (<30)."
        return "RSI is in a neutral range."

    @property
    def macd_comment(self) -> str:
        if self.macd > self.signal:
            return "MACD is above its signal line, suggesting bullish momentum."
        if self.macd < self.signal:
            return "MACD is below its signal line, suggesting bearish momentum."
        return "MACD and signal line are equal, indicating indecision."


def fetch_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
    if data.empty:
        raise ValueError("No data retrieved from Yahoo Finance. Check ticker or connection.")
    data = data.tz_localize(None)
    return data


def compute_indicators(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    rolling_std = df["Close"].rolling(window=20).std()
    df["Bollinger_Upper"] = df["SMA_20"] + (rolling_std * 2)
    df["Bollinger_Lower"] = df["SMA_20"] - (rolling_std * 2)

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["Signal"]

    return df


def summarize_indicators(df: pd.DataFrame) -> IndicatorSummary:
    latest = df.dropna().iloc[-1]
    return IndicatorSummary(
        latest_close=float(latest["Close"]),
        sma20=float(latest["SMA_20"]),
        sma50=float(latest["SMA_50"]),
        rsi=float(latest["RSI"]),
        macd=float(latest["MACD"]),
        signal=float(latest["Signal"]),
    )


def plot_indicators(df: pd.DataFrame, output_path: Path) -> None:
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True, gridspec_kw={"height_ratios": [3, 1, 1]})

    ax_price = axes[0]
    ax_price.plot(df.index, df["Close"], label="Close", color="#1f77b4", linewidth=1.5)
    ax_price.plot(df.index, df["SMA_20"], label="20-day SMA", color="#ff7f0e", linewidth=1.2)
    ax_price.plot(df.index, df["SMA_50"], label="50-day SMA", color="#2ca02c", linewidth=1.2)
    ax_price.fill_between(df.index, df["Bollinger_Lower"], df["Bollinger_Upper"], color="#c5b0d5", alpha=0.2, label="Bollinger Bands")
    ax_price.bar(df.index, df["Volume"] / 1e6, width=0.8, color="#7f7f7f", alpha=0.3, label="Volume (M)")
    ax_price.set_ylabel("Price (USD)")
    ax_price.set_title(f"{TICKER} – Last 3 Months Price & Indicators (NASDAQ)")
    ax_price.legend(loc="upper left", fontsize=9)

    ax_rsi = axes[1]
    ax_rsi.plot(df.index, df["RSI"], color="#d62728")
    ax_rsi.axhline(70, color="#8c564b", linestyle="--", linewidth=1)
    ax_rsi.axhline(30, color="#17becf", linestyle="--", linewidth=1)
    ax_rsi.fill_between(df.index, 70, df["RSI"], where=(df["RSI"] >= 70), color="#ff9896", alpha=0.3)
    ax_rsi.fill_between(df.index, df["RSI"], 30, where=(df["RSI"] <= 30), color="#98df8a", alpha=0.3)
    ax_rsi.set_ylabel("RSI")
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_title("Relative Strength Index (14-day)")

    ax_macd = axes[2]
    ax_macd.plot(df.index, df["MACD"], label="MACD", color="#9467bd")
    ax_macd.plot(df.index, df["Signal"], label="Signal", color="#8c564b", linestyle="--")
    ax_macd.bar(df.index, df["MACD_Hist"], label="Histogram", color="#c49c94")
    ax_macd.axhline(0, color="black", linewidth=0.8)
    ax_macd.set_ylabel("MACD")
    ax_macd.set_title("MACD (12, 26, 9)")
    ax_macd.legend(loc="upper left", fontsize=9)

    ax_macd.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax_macd.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    fig.autofmt_xdate()

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    data = fetch_data(TICKER, PERIOD, INTERVAL)
    indicators = compute_indicators(data)
    plot_indicators(indicators, OUTPUT_PATH)
    summary = summarize_indicators(indicators)

    rel_path = OUTPUT_PATH.relative_to(Path.cwd()) if OUTPUT_PATH.is_absolute() else OUTPUT_PATH
    print(f"Visualization saved to {rel_path}")
    print("\nLatest indicator snapshot:")
    print(f"  Close: ${summary.latest_close:.2f}")
    print(f"  20-day SMA: ${summary.sma20:.2f}")
    print(f"  50-day SMA: ${summary.sma50:.2f}")
    print(f"  RSI (14): {summary.rsi:.2f}")
    print(f"  MACD: {summary.macd:.3f}")
    print(f"  Signal: {summary.signal:.3f}")
    print(f"  Trend insight: {summary.trend}")
    print(f"  RSI insight: {summary.rsi_comment}")
    print(f"  MACD insight: {summary.macd_comment}")


if __name__ == "__main__":
    main()
