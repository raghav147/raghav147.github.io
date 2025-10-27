# INO Technical Visualization

This folder contains a utility script that builds a three-panel visualization of Inovio Pharmaceuticals (INO) using the last three months of daily data for the NASDAQ-listed stock.

## Files
- `ino_three_months.py` – Downloads daily OHLCV bars via Yahoo Finance, computes major technical indicators (20/50-day simple moving averages, Bollinger Bands, RSI, MACD), and saves a publication-ready PNG to `assets/image/ino_three_months_indicators.png`. The script also prints a brief textual summary of the latest indicator readings.

## Usage
1. Create and activate a Python environment with the required packages:
   ```bash
   pip install matplotlib pandas yfinance
   ```
2. Run the generator:
   ```bash
   python analysis/ino_three_months.py
   ```
3. Open `assets/image/ino_three_months_indicators.png` to review the visualization.

The figure highlights:
- **Price with 20/50-day SMAs and Bollinger Bands** to spot breakouts and trend alignment.
- **RSI (14)** with the standard 30/70 thresholds to flag overbought/oversold swings.
- **MACD (12, 26, 9)** including histogram bars to reveal momentum shifts.

> **Note:** The repository does not vendor dependencies or cache market data. Run the script from a networked environment to download the latest NASDAQ trading history for INO.
