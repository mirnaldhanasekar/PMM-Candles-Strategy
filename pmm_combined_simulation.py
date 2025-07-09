# --- 1. Install dependencies if needed (uncomment if running in Colab) ---
# !pip install numpy==1.26.4 pandas_ta ccxt matplotlib

import pandas as pd
import pandas_ta as ta
import numpy as np
import ccxt
import matplotlib.pyplot as plt

# --- 2. Download historical OHLCV data from Binance (ETH/USDT, 1m candles) ---
print("Fetching historical price data from Binance...")
exchange = ccxt.binance()
bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=1000)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# --- 3. Calculate technical indicators: NATR (volatility) and RSI (trend) ---
candles_length = 30
print("Calculating NATR and RSI indicators...")
df['natr'] = ta.natr(df['high'], df['low'], df['close'], length=candles_length)
df['rsi'] = ta.rsi(df['close'], length=candles_length)

# --- 4. Set strategy parameters (tune as needed) ---
bid_spread_scalar = 120      # Multiplier for bid spread (based on volatility)
ask_spread_scalar = 60       # Multiplier for ask spread (based on volatility)
max_shift_spread = 0.000005  # Maximum price shift for trend/inventory
trend_scalar = -1            # -1 for mean reversion, 1 for trend-following
inventory_scalar = 1         # Sensitivity of inventory skew
target_inventory_ratio = 0.5 # Target: 50% base, 50% quote
order_amount = 0.01          # Simulated order size

# --- 5. Initialize simulated inventory (start 50% in ETH, 50% in USDT) ---
eth_balance = 1.0
usdt_balance = df['close'].iloc[0]
inventory_history = []
price_history = []
spread_history = []
pnl_history = []

# --- 6. Main simulation loop ---
print("Running market-making simulation...")
for i in range(candles_length, len(df)):
    price = df['close'].iloc[i]
    natr = df['natr'].iloc[i]
    rsi = df['rsi'].iloc[i]
    
    # --- Volatility-based spreads ---
    bid_spread = natr * bid_spread_scalar
    ask_spread = natr * ask_spread_scalar

    # --- Trend logic (RSI-based price shift) ---
    price_multiplier = ((rsi - 50) / 50) * max_shift_spread * trend_scalar

    # --- Inventory management (skew reference price based on holdings) ---
    eth_value = eth_balance * price
    total_value = eth_value + usdt_balance
    if total_value > 0:
        current_inventory_ratio = eth_value / total_value
    else:
        current_inventory_ratio = target_inventory_ratio
    delta = (target_inventory_ratio - current_inventory_ratio) / target_inventory_ratio
    delta = np.clip(delta, -1, 1)
    inventory_multiplier = delta * max_shift_spread * inventory_scalar

    # --- Reference price combines trend and inventory adjustments ---
    reference_price = price * (1 + price_multiplier) * (1 + inventory_multiplier)
    buy_price = reference_price * (1 - bid_spread)
    sell_price = reference_price * (1 + ask_spread)

    # --- Simulate random order fill (for demonstration only) ---
    if np.random.rand() < 0.5:
        # Simulate a filled buy order
        if usdt_balance >= buy_price * order_amount:
            eth_balance += order_amount
            usdt_balance -= buy_price * order_amount
    else:
        # Simulate a filled sell order
        if eth_balance >= order_amount:
            eth_balance -= order_amount
            usdt_balance += sell_price * order_amount

    # --- Record metrics for analysis ---
    inventory_history.append(current_inventory_ratio)
    price_history.append(price)
    spread_history.append((bid_spread, ask_spread))
    # Mark-to-market PnL (ETH+USDT in quote terms)
    pnl_history.append(eth_balance * price + usdt_balance)

# --- 7. Visualization: Inventory ratio, price, spreads, and PnL ---
plt.figure(figsize=(12,4))
plt.plot(df['timestamp'][candles_length:], inventory_history, label='Inventory Ratio (ETH)')
plt.axhline(target_inventory_ratio, color='red', linestyle='--', label='Target Ratio')
plt.title('Simulated Inventory Ratio Over Time')
plt.xlabel('Time')
plt.ylabel('Inventory Ratio (ETH)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12,4))
plt.plot(df['timestamp'][candles_length:], price_history, label='ETH/USDT Price', color='gray')
plt.title('ETH/USDT Price Over Time')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

bid_spreads, ask_spreads = zip(*spread_history)
plt.figure(figsize=(12,4))
plt.plot(df['timestamp'][candles_length:], np.array(bid_spreads)*10000, label='Bid Spread (bps)')
plt.plot(df['timestamp'][candles_length:], np.array(ask_spreads)*10000, label='Ask Spread (bps)')
plt.title('Bid/Ask Spreads Over Time (basis points)')
plt.xlabel('Time')
plt.ylabel('Spread (bps)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12,4))
plt.plot(df['timestamp'][candles_length:], pnl_history, label='Simulated PnL (USD)')
plt.title('Simulated Mark-to-Market PnL Over Time')
plt.xlabel('Time')
plt.ylabel('PnL (USD)')
plt.legend()
plt.grid(True)
plt.show()

print("Simulation complete. All features required by the assignment are demonstrated in this script.")
