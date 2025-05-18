# InsideBar_Strategy

This project demonstrates a framework for backtesting and visualizing the Inside Bar Strategy on cryptocurrency price data using Python. The script processes historical price data (e.g., BTC/USD 4-hour timeframe), applies the Inside Bar Strategy (logic masked for proprietary reasons), and generates insightful visualizations to evaluate performance.

## Results

### Visualizations:

#### Equity Curve: Shows capital growth over time with max drawdown highlighted.
![equity_curve_BTC4h](https://github.com/user-attachments/assets/7458a855-80bb-4dbf-98c2-dc88191f0065)



#### Monthly Profit Percentage: Bar chart of monthly performance.
![monthly_profit_pct_BTC4h](https://github.com/user-attachments/assets/cea4326a-82bb-4a9c-94a9-0020f7763ca3)



#### OHLC Chart: Candlestick chart with buy/sell signals.
![ohlc_chart_fixed_BTC4h](https://github.com/user-attachments/assets/abf71279-8e48-428d-90a9-40213752ed47)



#### Summary Dashboard: A consolidated view of key metrics, equity curve, and monthly profits.
![summary_dashboard_BTC4h](https://github.com/user-attachments/assets/d151f438-a36c-4c21-b64c-84ae0695b44d)


The following results were obtained by running the original (unmasked) script on BTC/USD 4-hour data:

### Backtest Results:

- Initial Capital: $10000.00
- Final Capital: $50398.50
- Profit Percentage: 403.99%
- Total Trades: 119
- Win Rate: 31.93%
- Total Profit: $40398.50
- Average Profit Per Trade: $342.36
- Max Drawdown: $16184.50
- Max Drawdown Percentage: 29.28%

#### Month-wise Profit Percentage:
- 2024-01: 0.00%
- 2024-02: 40.91%
- 2024-03: 64.31%
- 2024-04: 18.52%
- 2024-05: -25.59%
- 2024-06: -8.87%
- 2024-07: -51.85%
- 2024-08: 91.86%
- 2024-09: 53.45%
- 2024-10: 33.80%
- 2024-11: 60.45%
- 2024-12: 48.30%
- 2025-01: -24.57%
- 2025-03: 88.39%
- 2025-04: 47.32%
- 2025-05: -32.46%

## Disclaimer

This script is not for any kind of use. Trading involves significant risk, and past performance is not indicative of future results.
