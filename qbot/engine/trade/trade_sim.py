from qbot.engine.trade.trade_base import BaseTradeEngine


class SimTradeEngine(BaseTradeEngine):
    _account_suffix = "SIM"
    engine_name = "SimTradeEngine"


if __name__ == "__main__":
    from qbot.common.logging.logger import LOGGER as logger

    trade_opts = {
        "class": "虚拟盘",
        "platform": "掘金",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }

    sim_trade_engine = SimTradeEngine(trade_opts=trade_opts, syslog_obj=None)

    # sim_trade_engine.login()
    sim_trade_engine.get_cash()
    sim_trade_engine.get_positions()
    sim_trade_engine.start_trade()
    sim_trade_engine.close()
