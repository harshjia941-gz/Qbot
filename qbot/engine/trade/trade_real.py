from qbot.engine.trade.trade_base import BaseTradeEngine


class RealTradeEngine(BaseTradeEngine):
    _account_suffix = "REAL"
    engine_name = "RealTradeEngine"


if __name__ == "__main__":
    from qbot.common.file_utils import file2dict
    from qbot.common.logging.logger import LOGGER as logger

    trade_opts = {
        "class": "实盘",
        "platform": "掘金",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }

    real_trade_engine = RealTradeEngine(trade_opts=trade_opts, syslog_obj=None)
    real_trade_engine.login()
    real_trade_engine.get_cash()
    real_trade_engine.get_positions()
    real_trade_engine.start_trade()
    real_trade_engine.close()
