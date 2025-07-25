# PMM Candles Strategy

A creative **Passive Market Making (PMM)** strategy that uses candlestick data and RSI indicators to place intelligent buy and sell orders on the Binance exchange in paper trade mode. Built on top of the Hummingbot framework, this repository also provides a standalone simulation script that demonstrates advanced market-making logic without requiring Hummingbot.

## ✅ Key Features

- **1-Minute Candlestick Data:** Uses the `candles_feed` module to access and analyze 1-minute interval candlestick data.
- **Dynamic RSI Calculation:** Continuously computes the Relative Strength Index (RSI) for momentum-based trading decisions.
- **Volatility-Based Spread Adjustment:** Spreads are dynamically set using the NATR indicator, adapting to market volatility.
- **Trend Logic:** Uses RSI to shift reference prices for trend-following or mean-reversion behavior.
- **Inventory Management:** Skews pricing based on your current vs. target holdings to manage risk and exposure.
- **Configurable Limit Orders:** Places buy and sell orders with customizable spreads.
- **Dual Operation Modes:**  
  - Runs inside the Hummingbot framework as a custom strategy script.
  - Can be executed as a standalone Python simulation (no Hummingbot required).
- **Backtesting and Simulation Ready:** Suitable for testing on historical data or in simulated environments.
- **Performance Visualization:** Plots inventory, price, spreads, and PnL for diagnostics.

## 🚀 How to Run the Strategy

### 1. Clone the Repository

```bash
git clone https://github.com/mirnaldhanasekar/PMM-Candles-Strategy.git
cd PMM-Candles-Strategy
```

### 2. Create & Activate Environment

Ensure you have the Hummingbot environment activated:

```bash
conda activate hummingbot
```

*(If the environment is not yet created, follow Hummingbot’s official setup instructions.)*

### 3. Run in Standalone Simulation Mode

To run the advanced simulation script without Hummingbot:

```bash
python pmm_combined_simulation.py
```

**Dependencies:**  
Install required packages if needed:

```bash
pip install numpy==1.26.4 pandas_ta ccxt matplotlib
```

*(If using Google Colab, add the install lines at the top and restart the runtime after installing.)*

### 4. Run Inside Hummingbot

To run the strategy inside the Hummingbot client:

- Place your strategy script file inside the `scripts/` folder of your Hummingbot installation.
- Start the Hummingbot CLI:

  ```bash
  python bin/hummingbot.py
  ```

- Use the CLI to configure and run your strategy:

  ```
  script start pmm_candles_standalone
  ```

  *(Omit the `.py` extension when using the `script start` command.)*

## 📈 Example Output

```
📊 Latest Price: 2030.6
🟢 Buy at 2026.54 | 🔴 Sell at 2034.67
📈 RSI: 66.86
```

When running the simulation script, you’ll also see plots for:

- Inventory ratio over time (shows how well the strategy maintains your target balance)
- ETH/USDT price evolution
- Bid/ask spreads in basis points (bps)
- Simulated mark-to-market PnL

## 🗂️ Features Table

| Script Name                  | Volatility-Based Spread | Trend Logic (RSI) | Inventory Management | How to Run                                  |
|------------------------------|:----------------------:|:-----------------:|:-------------------:|---------------------------------------------|
| `pmm_candles.py`             | No                     | Yes               | No                  | Hummingbot only                             |
| `pmm-volatility-spread.py`   | Yes                    | No                | No                  | Hummingbot only                             |
| `pmm_trend_shift.py`         | Yes                    | Yes               | No                  | Hummingbot only                             |
| `pmm-inventory-shift.py`     | Yes                    | Yes               | Yes                 | Hummingbot only                             |
| `pmm_combined_simulation.py` | Yes                    | Yes               | Yes                 | Python/Colab, no Hummingbot required        |

## 📝 Summary

- This repository demonstrates a robust, feature-rich PMM strategy using both Hummingbot and standalone simulation.
- All advanced requirements—volatility-based spreads, trend logic, inventory management, and clear visualization—are included.
- The simulation script (`pmm_combined_simulation.py`) is fully documented and ready for direct use in Python or Colab, making it easy to test, review, and extend.

**For more details, see the code and comments in each script.**

[1] https://pplx-res.cloudinary.com/image/private/user_uploads/53709042/2502fd27-68de-44ac-afab-6eb961546d1f/image.jpg
