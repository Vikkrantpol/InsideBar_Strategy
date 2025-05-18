```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import os

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['time', 'open', 'high', 'low', 'volume']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing columns: {missing}")
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[required_columns].sort_values('time')
        df = df.reset_index(drop=True)
        if 'close' not in df.columns:
            df['close'] = df['open']
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found in the current directory.")
        raise
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def find_inside_bars(df):
    # [Proprietary Logic Masked]
    # This function identifies specific candlestick patterns for trading signals.
    # In the original implementation, it marks bars based on certain criteria.
    print("Trading signal logic is proprietary and has been masked.")
    # Placeholder: Return the dataframe with dummy columns
    df['Inside_Bar'] = False
    df['Mother_Bar_high'] = np.nan
    df['Mother_Bar_low'] = np.nan
    return df

def backtest_inside_bar(df, risk_reward_ratio=2.0, trade_size=1):
    # [Proprietary Logic Masked]
    # This function implements the backtesting of the trading strategy based on signals.
    # It generates trades with entry, stop-loss, take-profit, and exit details.
    print("Backtesting logic is proprietary and has been masked.")
    # Placeholder: Return an empty trades dataframe with the expected structure
    trades = []
    trades_df = pd.DataFrame(trades, columns=[
        'Entry_time', 'Type', 'Entry_Price', 'Stop_Loss', 'Take_Profit',
        'Exit_Price', 'Exit_time', 'Profit'
    ])
    return trades_df

def calculate_metrics(trades_df, initial_capital=10000):
    if trades_df.empty:
        return {
            'Total_Trades': 0,
            'Win_Rate': 0,
            'Total_Profit': 0,
            'Avg_Profit_Per_Trade': 0,
            'Max_Drawdown': 0,
            'Max_Drawdown_Pct': 0,
            'Initial_Capital': initial_capital,
            'Final_Capital': initial_capital,
            'Profit_Percentage': 0,
            'Monthly_Profits': {}
        }
    total_trades = len(trades_df)
    wins = len(trades_df[trades_df['Profit'] > 0])
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
    total_profit = trades_df['Profit'].sum()
    avg_profit = trades_df['Profit'].mean() if total_trades > 0 else 0
    equity = initial_capital + trades_df['Profit'].cumsum()
    drawdowns = equity.cummax() - equity
    max_drawdown = drawdowns.max() if not drawdowns.empty else 0
    peak_capital = equity.max() if not equity.empty else initial_capital
    max_drawdown_pct = (max_drawdown / peak_capital) * 100 if peak_capital > 0 else 0
    final_capital = initial_capital + total_profit
    profit_percentage = ((final_capital - initial_capital) / initial_capital) * 100
    trades_df['Month'] = trades_df['Exit_time'].dt.to_period('M')
    monthly_profits = trades_df.groupby('Month')['Profit'].sum()
    monthly_profit_pct = (monthly_profits / initial_capital) * 100
    monthly_profits_dict = monthly_profit_pct.to_dict()
    return {
        'Total_Trades': total_trades,
        'Win_Rate': win_rate,
        'Total_Profit': total_profit,
        'Avg_Profit_Per_Trade': avg_profit,
        'Max_Drawdown': max_drawdown,
        'Max_Drawdown_Pct': max_drawdown_pct,
        'Initial_Capital': initial_capital,
        'Final_Capital': final_capital,
        'Profit_Percentage': profit_percentage,
        'Monthly_Profits': monthly_profits_dict
    }

def plot_equity_curve(trades_df, initial_capital=10000, max_drawdown=0, max_drawdown_pct=0):
    try:
        if trades_df.empty:
            print("No trades to plot for equity curve.")
            return
        equity = initial_capital + trades_df['Profit'].cumsum()
        plt.figure(figsize=(14, 7))
        plt.plot(trades_df['Exit_time'], equity, label='Equity Curve', color='blue', linewidth=2)
        peak_capital = equity.max()
        drawdown_level = peak_capital - max_drawdown
        plt.axhline(y=drawdown_level, color='red', linestyle='--', alpha=0.5, 
                    label=f'Max Drawdown: ${max_drawdown:.2f} ({max_drawdown_pct:.2f}%)')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Capital (USD)', fontsize=12)
        plt.title('Equity Curve for Crypto Trading Strategy (BTC/USD 4h)', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        output_path = 'equity_curve_BTC4h.png'
        plt.savefig(output_path, dpi=300)
        print(f"Equity curve saved as: {os.path.abspath(output_path)}")
        plt.show()
    except Exception as e:
        print(f"Failed to plot equity curve: {str(e)}")

def plot_monthly_profit(metrics):
    try:
        if not metrics['Monthly_Profits']:
            print("No monthly profits to plot.")
            return
        months = [str(month) for month in metrics['Monthly_Profits'].keys()]
        profits = list(metrics['Monthly_Profits'].values())
        colors = ['green' if p >= 0 else 'red' for p in profits]
        plt.figure(figsize=(16, 8))
        bars = plt.bar(months, profits, color=colors, edgecolor='black', width=0.4)
        for bar, profit in zip(bars, profits):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + (0.5 if yval >= 0 else -2.5), 
                     f'{profit:.1f}%', ha='center', va='bottom' if yval >= 0 else 'top', fontsize=10)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Profit Percentage (%)', fontsize=12)
        plt.title('Monthly Profit Percentage for Crypto Trading Strategy (BTC/USD 4h)', fontsize=14)
        plt.grid(True, axis='y', alpha=0.3)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        output_path = 'monthly_profit_pct_BTC4h.png'
        plt.savefig(output_path, dpi=300)
        print(f"Monthly profit percentage plot saved as: {os.path.abspath(output_path)}")
        plt.show()
    except Exception as e:
        print(f"Failed to plot monthly profit percentage: {str(e)}")

def plot_candlestick_chart(df, trades_df):
    #Masked

def plot_summary_dashboard(metrics, trades_df, initial_capital=10000):
    try:
        fig = plt.figure(figsize=(16, 10), facecolor='white')
        plt.suptitle('Crypto Trading Strategy Dashboard (BTC/USD 4h)', fontsize=20, fontweight='bold', y=0.98)
        ax_metrics = fig.add_axes([0.05, 0.55, 0.45, 0.35])
        ax_metrics.axis('off')
        metrics_text = (
            f"Initial Capital: ${metrics['Initial_Capital']:.2f}\n"
            f"Final Capital: ${metrics['Final_Capital']:.2f}\n"
            f"Profit Percentage: {metrics['Profit_Percentage']:.2f}%\n"
            f"Total Trades: {metrics['Total_Trades']:.0f}\n"
            f"Win Rate: {metrics['Win_Rate']:.2f}%\n"
            f"Total Profit: ${metrics['Total_Profit']:.2f}\n"
            f"Avg Profit Per Trade: ${metrics['Avg_Profit_Per_Trade']:.2f}\n"
            f"Max Drawdown: ${metrics['Max_Drawdown']:.2f}\n"
            f"Max Drawdown Pct: {metrics['Max_Drawdown_Pct']:.2f}%"
        )
        ax_metrics.text(0.05, 0.95, metrics_text, fontsize=12, va='top', ha='left', 
                       bbox=dict(facecolor='lightgrey', edgecolor='black', boxstyle='round,pad=0.5'))
        ax_equity = fig.add_axes([0.55, 0.55, 0.4, 0.35])
        equity = initial_capital + trades_df['Profit'].cumsum()
        ax_equity.plot(trades_df['Exit_time'], equity, label='Equity Curve', color='blue', linewidth=2)
        ax_equity.set_title('Equity Curve', fontsize=14)
        ax_equity.set_xlabel('Time', fontsize=10)
        ax_equity.set_ylabel('Capital (USD)', fontsize=10)
        ax_equity.grid(True, alpha=0.3)
        ax_equity.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax_equity.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax_equity.get_xticklabels(), rotation=45, fontsize=8)
        plt.setp(ax_equity.get_yticklabels(), fontsize=8)
        ax_monthly = fig.add_axes([0.05, 0.05, 0.9, 0.35])
        if metrics['Monthly_Profits']:
            months = [str(month) for month in metrics['Monthly_Profits'].keys()]
            profits = list(metrics['Monthly_Profits'].values())
            colors = ['green' if p >= 0 else 'red' for p in profits]
            bars = ax_monthly.bar(months, profits, color=colors, edgecolor='black', width=0.4)
            for bar, profit in zip(bars, profits):
                yval = bar.get_height()
                ax_monthly.text(bar.get_x() + bar.get_width()/2, yval + (0.5 if yval >= 0 else -2.5), 
                               f'{profit:.1f}%', ha='center', va='bottom' if yval >= 0 else 'top', fontsize=8)
            ax_monthly.set_title('Monthly Profit Percentage', fontsize=14)
            ax_monthly.set_xlabel('Month', fontsize=10)
            ax_monthly.set_ylabel('Profit Percentage (%)', fontsize=10)
            ax_monthly.grid(True, axis='y', alpha=0.3)
            plt.setp(ax_monthly.get_xticklabels(), rotation=45, fontsize=8)
            plt.setp(ax_monthly.get_yticklabels(), fontsize=8)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        output_path = 'summary_dashboard_BTC4h.png'
        plt.savefig(output_path, dpi=600, bbox_inches='tight')
        print(f"Summary dashboard saved as: {os.path.abspath(output_path)}")
        plt.show()
    except Exception as e:
        print(f"Failed to plot summary dashboard: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    file_path = "BTCdata4h.csv"
    initial_capital = 10000
    try:
        df = load_data(file_path)
        df = find_inside_bars(df)
        trades_df = backtest_inside_bar(df, risk_reward_ratio=2.0, trade_size=1)
        metrics = calculate_metrics(trades_df, initial_capital)
        print("Backtest Results:")
        print(f"Initial Capital: ${metrics['Initial_Capital']:.2f}")
        print(f"Final Capital: ${metrics['Final_Capital']:.2f}")
        print(f"Profit Percentage: {metrics['Profit_Percentage']:.2f}%")
        print(f"Total Trades: {metrics['Total_Trades']:.0f}")
        print(f"Win Rate: {metrics['Win_Rate']:.2f}%")
        print(f"Total Profit: ${metrics['Total_Profit']:.2f}")
        print(f"Average Profit Per Trade: ${metrics['Avg_Profit_Per_Trade']:.2f}")
        print(f"Max Drawdown: ${metrics['Max_Drawdown']:.2f}")
        print(f"Max Drawdown Percentage: {metrics['Max_Drawdown_Pct']:.2f}%")
        print("\nMonth-wise Profit Percentage:")
        for month, profit_pct in sorted(metrics['Monthly_Profits'].items()):
            print(f"{month}: {profit_pct:.2f}%")
        trades_df.to_csv("trades_output.csv", index=False)
        print("Trades saved to 'trades_output.csv'")
        plot_equity_curve(trades_df, initial_capital, 
                         metrics['Max_Drawdown'], metrics['Max_Drawdown_Pct'])
        plot_monthly_profit(metrics)
        plot_candlestick_chart(df, trades_df)
        plot_summary_dashboard(metrics, trades_df, initial_capital)
    except Exception as e:
        print(f"Script execution failed: {str(e)}")
```
