import logging
from decimal import Decimal
from typing import Dict, List

from hummingbot.core.data_type.common import OrderType, PriceType, TradeType
from hummingbot.core.data_type.order_candidate import OrderCandidate
from hummingbot.core.event.events import OrderFilledEvent
from hummingbot.strategy.script_strategy_base import ScriptStrategyBase
from hummingbot.data_feed.candles_feed.candles_factory import CandlesFactory, CandlesConfig
from hummingbot.connector.connector_base import ConnectorBase


class PMMCandles(ScriptStrategyBase):
    """
    BotCamp - Market Making Strategies
    Description:
    The bot extends the Simple PMM example script by incorporating the Candles Feed and creating a custom status function that displays it.
    """
    bid_spread = 0.0001
    ask_spread = 0.0001
    order_refresh_time = 15
    order_amount = 0.01
    create_timestamp = 0
    trading_pair = "ETH-USDT"
    exchange = "binance_paper_trade"
    price_source = PriceType.MidPrice

    # Candles params
    candle_exchange = "binance"
    candles_interval = "1m"
    candles_length = 30
    max_records = 1000

    # Initializes candles
    candles = CandlesFactory.get_candle(CandlesConfig(connector=candle_exchange,
                                                      trading_pair=trading_pair,
                                                      interval=candles_interval,
                                                      max_records=max_records))

    # Markets defines which order books (exchange / pair) to connect to
    markets = {exchange: {trading_pair}}

    def __init__(self, connectors: Dict[str, ConnectorBase]):
        super().__init__(connectors)
        print("✅ PMMCandles Strategy Initialized")
        self.candles.start()

    def on_stop(self):
        self.candles.stop()

    def on_tick(self):
        if self.create_timestamp <= self.current_timestamp:
            self.cancel_all_orders()
            proposal: List[OrderCandidate] = self.create_proposal()
            proposal_adjusted: List[OrderCandidate] = self.adjust_proposal_to_budget(proposal)
            self.place_orders(proposal_adjusted)
            self.create_timestamp = self.order_refresh_time + self.current_timestamp

    def get_candles_with_features(self):
        candles_df = self.candles.candles_df
        candles_df.ta.rsi(length=self.candles_length, append=True)
        return candles_df

    def create_proposal(self) -> List[OrderCandidate]:
        ref_price = self.connectors[self.exchange].get_price_by_type(self.trading_pair, self.price_source)
        buy_price = ref_price * Decimal(1 - self.bid_spread)
        sell_price = ref_price * Decimal(1 + self.ask_spread)

        buy_order = OrderCandidate(trading_pair=self.trading_pair, is_maker=True, order_type=OrderType.LIMIT,
                                   order_side=TradeType.BUY, amount=Decimal(self.order_amount), price=buy_price)

        sell_order = OrderCandidate(trading_pair=self.trading_pair, is_maker=True, order_type=OrderType.LIMIT,
                                    order_side=TradeType.SELL, amount=Decimal(self.order_amount), price=sell_price)

        return [buy_order, sell_order]

    def adjust_proposal_to_budget(self, proposal: List[OrderCandidate]) -> List[OrderCandidate]:
        proposal_adjusted = self.connectors[self.exchange].budget_checker.adjust_candidates(proposal, all_or_none=True)
        return proposal_adjusted

    def place_orders(self, proposal: List[OrderCandidate]) -> None:
        for order in proposal:
            self.place_order(connector_name=self.exchange, order=order)

    def place_order(self, connector_name: str, order: OrderCandidate):
        if order.order_side == TradeType.SELL:
            self.sell(connector_name=connector_name, trading_pair=order.trading_pair, amount=order.amount,
                      order_type=order.order_type, price=order.price)
        elif order.order_side == TradeType.BUY:
            self.buy(connector_name=connector_name, trading_pair=order.trading_pair, amount=order.amount,
                     order_type=order.order_type, price=order.price)

    def cancel_all_orders(self):
        for order in self.get_active_orders(connector_name=self.exchange):
            self.cancel(self.exchange, order.trading_pair, order.client_order_id)

    def did_fill_order(self, event: OrderFilledEvent):
        msg = (f"{event.trade_type.name} {round(event.amount, 2)} {event.trading_pair} {self.exchange} at {round(event.price, 2)}")
        self.log_with_clock(logging.INFO, msg)
        self.notify_hb_app_with_timestamp(msg)

    def format_status(self) -> str:
        """
        Returns status of the current strategy and displays candles feed info
        """
        if not self.ready_to_trade:
            return "Market connectors are not ready."
        lines = []

        balance_df = self.get_balance_df()
        lines.extend(["", "  Balances:"] + ["    " + line for line in balance_df.to_string(index=False).split("\n")])

        try:
            df = self.active_orders_df()
            lines.extend(["", "  Orders:"] + ["    " + line for line in df.to_string(index=False).split("\n")])
        except ValueError:
            lines.extend(["", "  No active maker orders."])

        lines.extend(["\n----------------------------------------------------------------------\n"])
        candles_df = self.get_candles_with_features()
        lines.extend([f"  Candles: {self.candles.name} | Interval: {self.candles.interval}", ""])
        lines.extend(["    " + line for line in candles_df.tail(self.candles_length).iloc[::-1].to_string(index=False).split("\n")])

        return "\n".join(lines)


# ✅ Simple test section when run directly
if __name__ == "__main__":
    print("✅ PMMCandles strategy script loaded.")
    print("⚠️  This is a strategy class meant to be used inside Hummingbot.")
    print("💡 To use it, create a strategy config file and run via Hummingbot CLI.")
