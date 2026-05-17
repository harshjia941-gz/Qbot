"""
RSI (Relative Strength Index) Strategy for Backtrader.
Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought).
"""
import backtrader as bt


class RSIStrategy(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("rsi_lower", 40),
        ("rsi_upper", 60),
        ("printlog", False),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi[0] < self.params.rsi_lower:
                self.order = self.buy()
        else:
            if self.rsi[0] > self.params.rsi_upper:
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY @ {order.executed.price:.2f}")
            elif order.issell():
                self.log(f"SELL @ {order.executed.price:.2f}")
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order failed")
        self.order = None

    def log(self, txt):
        if self.params.printlog:
            dt = self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")
