import random
import pandas as pd
import pandas_ta as ta
from decimal import Decimal

class SimplePMMCandles:
    def __init__(self, bid_spread=0.001, ask_spread=0.001, order_amount=1):
        self.bid_spread = Decimal(bid_spread)
        self.ask_spread = Decimal(ask_spread)
        self.order_amount = Decimal(order_amount)
        self.price_history = []
        self.generate_initial_prices()

    def generate_initial_prices(self):
        # Simulate 30 candle prices
        price = 2000
        for _ in range(30):
            price += random.uniform(-5, 5)
            self.price_history.append(price)

    def update_candles(self):
        # Simulate a new candle price
        last_price = self.price_history[-1]
        new_price = last_price + random.uniform(-10, 10)
        self.price_history.append(new_price)
        if len(self.price_history) > 100:
            self.price_history.pop(0)

    def calculate_rsi(self):
        df = pd.DataFrame({"close": self.price_history})
        df["RSI"] = ta.rsi(df["close"], length=14)
        return df

    def create_order_proposal(self, mid_price):
        buy_price = Decimal(mid_price) * (1 - self.bid_spread)
        sell_price = Decimal(mid_price) * (1 + self.ask_spread)
        return {"buy": round(buy_price, 2), "sell": round(sell_price, 2)}

    def run_once(self):
        self.update_candles()
        df = self.calculate_rsi()
        mid_price = self.price_history[-1]
        order_proposal = self.create_order_proposal(mid_price)

        print(f"\n📊 Latest Price: {round(mid_price, 2)}")
        print(f"🟢 Buy at {order_proposal['buy']} | 🔴 Sell at {order_proposal['sell']}")
        print(f"📈 RSI: {round(df['RSI'].iloc[-1], 2)}")

    def run_simulation(self, iterations=20):
        print("🚀 Running Simple PMM Candles Simulation...\n")
        for _ in range(iterations):
            self.run_once()


if __name__ == "__main__":
    bot = SimplePMMCandles(bid_spread=0.002, ask_spread=0.002, order_amount=0.01)
    bot.run_simulation()
