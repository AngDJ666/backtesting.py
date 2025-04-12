import pandas as pd
from scipy.stats import zscore
import numpy as np

def generate_signals_advanced(df, bull_state, bear_state, z_threshold=0.5, hold_period=3, stop_loss_atr_multiplier=1.5):
    # Calculate Z-score for inflows
    df['inflow_z'] = pd.Series(zscore(df['CQ_inflow_mean'] - df['CQ_inflow_mean_ma7']), index=df.index).fillna(0)
    
    # Calculate recent return over the last 3 periods (days)
    df['recent_return'] = df['Close'].pct_change(3).fillna(0)

    # Calculate ATR (Average True Range) for dynamic stop-loss
    df['ATR'] = df['Close'].rolling(window=14).apply(lambda x: np.max(x) - np.min(x), raw=False)
    df['ATR'] = df['ATR'].fillna(0)

    signals = []
    position = 0
    entry_price = 0
    hold_timer = 0

    for i in range(len(df)):
        # Get the current regime (bull or bear state)
        regime = df['Regime'].iloc[i]
        
        # Get the Z-score, recent return, price, and ATR for the current row
        inflow_z = df['inflow_z'].iloc[i]
        price = df['Close'].iloc[i]
        recent_return = df['recent_return'].iloc[i]
        atr = df['ATR'].iloc[i]

        # Default signal is to maintain the current position
        signal = position

        # Calculate dynamic stop-loss based on ATR
        stop_loss_pct = atr * stop_loss_atr_multiplier

        # Stop-loss logic (if price moves against the position by more than the stop-loss percentage)
        if position != 0 and abs((price - entry_price) / entry_price) >= stop_loss_pct:
            signal = 0
            position = 0
            hold_timer = 0

        # Entry condition (Z-score + momentum)
        elif hold_timer == 0:
            # Bull market conditions: Z-score and recent return
            if regime == bull_state and inflow_z < -z_threshold and recent_return > 0:
                signal = 1  # Enter long position
                entry_price = price
                hold_timer = hold_period
            # Bear market conditions: Z-score and recent return
            elif regime == bear_state and inflow_z > z_threshold and recent_return < 0:
                signal = -1  # Enter short position
                entry_price = price
                hold_timer = hold_period
            else:
                signal = 0  # No position

        # Countdown the hold period
        if hold_timer > 0:
            hold_timer -= 1

        # Append the signal to the list of signals
        signals.append(signal)
        position = signal  # Update the position

    # Add the generated signals to the DataFrame
    df['Signal'] = signals
    return df
































