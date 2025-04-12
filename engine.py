import pandas as pd
import numpy as np

def backtest(df, initial_capital=100000, fee_rate=0.0006):
    position = 0
    equity = initial_capital
    equity_curve = [equity]  # Initialize equity curve with initial capital
    trade_count = 0

    for i in range(1, len(df)):
        signal = df['Signal'].iloc[i]
        price_change = df['Close'].iloc[i] - df['Close'].iloc[i - 1]
        
        if position != 0:
            equity += position * price_change  # Update equity
        
        # Apply fee when a trade happens (buy/sell)
        if signal != position:
            equity *= (1 - fee_rate)  # Apply fee
            position = signal  # Update position
            trade_count += 1
        
        equity_curve.append(equity)

    # Ensure the length of equity_curve matches the DataFrame index
    equity_curve.extend([equity_curve[-1]] * (len(df) - len(equity_curve)))  # Pad with the last value

    df['Equity'] = pd.Series(equity_curve, index=df.index)  # Ensure matching index

    return df, calculate_performance(df, initial_capital, trade_count)

def calculate_performance(df, initial_capital, trade_count):
    equity = df['Equity'].values
    returns = np.diff(equity) / equity[:-1]
    sharpe = (returns.mean() / returns.std()) * np.sqrt(8760) if returns.std() > 0 else 0
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    max_dd = drawdown.min()
    trade_freq = trade_count / len(df)
    return {
        'Final Equity': float(equity[-1]),
        'Total Return': (equity[-1] - initial_capital) / initial_capital,
        'Sharpe Ratio': sharpe,
        'Max Drawdown': abs(max_dd),
        'Trade Count': trade_count,
        'Trade Frequency': trade_freq
    }



