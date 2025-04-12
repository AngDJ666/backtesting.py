import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from data_loader import load_and_merge_data
from strategy import generate_signals_advanced
from engine import backtest

# === Load & prepare data ===
df = load_and_merge_data()

# === HMM Regime Detection ===
features = df[['return', 'CQ_inflow_total']].values
hmm = GaussianHMM(n_components=3, covariance_type='diag', n_iter=100, random_state=42)
hmm.fit(features)
states = hmm.predict(features)
df['Regime'] = states

# === Label regimes ===
state_means = {s: df[df['Regime'] == s]['return'].mean() for s in np.unique(states)}
bull_state = max(state_means, key=state_means.get)
bear_state = min(state_means, key=state_means.get)

# === Generate Signals ===
df = generate_signals_advanced(df, bull_state, bear_state)

# === Run Backtest ===
df, performance = backtest(df)

# === Plot Results ===
plt.figure(figsize=(12, 5))
plt.plot(df.index, df['Equity'], label='Equity Curve')
plt.title("Equity Curve (Modular HMM Strategy)")
plt.xlabel("Time")
plt.ylabel("Equity ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# === Print Performance ===
print("\n📊 Performance Summary")
for k, v in performance.items():
    print(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}")










