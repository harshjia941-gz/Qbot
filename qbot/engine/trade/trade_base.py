import easytrader

from qbot.common.file_utils import file2dict
from qbot.common.logging.logger import LOGGER as logger


class BaseTradeEngine:
    _account_suffix: str = ""
    engine_name: str = "BaseTradeEngine"

    def __init__(self, trade_opts: dict, syslog_obj, user=None):
        if syslog_obj:
            self.syslog = syslog_obj
        else:
            logger.error("syslog_obj is null.")
            return

        self.syslog.re_print(f"{self.engine_name} start init ...\n")

        if trade_opts:
            logger.info(trade_opts)
        else:
            logger.error("trade_opts is empty.")
            return

        self.trade_opts = trade_opts
        self.trade_engine = None

        if not user:
            accounts = self._get_accounts(trade_opts["trade_type"])
            if accounts is None:
                logger.error("当前还不支持该交易标的, 请联系微信 Yida_Zhang2")
                return

            trade_type = trade_opts["trade_type"]
            if trade_type == "股票":
                self._init_stock(accounts, trade_opts)
            elif trade_type == "期货":
                self._init_futures(accounts, trade_opts)
            elif trade_type == "BTC":
                self._init_btc(accounts, trade_opts)
            # 基金, 期权 — accounts loaded only, no engine created
        else:
            self.user = user

        if not self.trade_engine:
            logger.error("trade engine is null")
            return

    def _get_accounts(self, trade_type: str):
        from qbot.engine import config

        type_map = {
            "股票": f"STOCK_{self._account_suffix}_ACCOUNT",
            "基金": f"FUNDS_{self._account_suffix}_ACCOUNT",
            "期货": f"FUTURES_{self._account_suffix}_ACCOUNT",
            "BTC": f"BTC_{self._account_suffix}_ACCOUNT",
            "期权": f"OPTIONS_{self._account_suffix}_ACCOUNT",
        }
        var_name = type_map.get(trade_type)
        if not var_name:
            return None
        return file2dict(getattr(config, var_name))

    def _init_stock(self, accounts, trade_opts):
        from qbot.engine.trade.engine_apis.stocks.stock_engine import (
            StockTradeEngine,
        )

        if trade_opts["platform"] not in accounts:
            logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")
            return

        self.trade_engine = StockTradeEngine(
            account=accounts[trade_opts["platform"]],
            trade_opts=trade_opts,
            syslog_obj=self.syslog,
        )
        self.trade_engine.login()

        self._setup_easytrader(accounts, trade_opts["platform"])

    def _setup_easytrader(self, accounts, platform):
        platform_map = {
            "华泰证券": "ht_client",
            "通达信": "tongda",
            "银河证券": "yinhe",
            "同花顺": "tonghuashun",
            "雪球": "xuqiu",
        }
        if platform in platform_map:
            self.user = easytrader.use(platform_map[platform])
            self.user.prepare(
                platform,
                username=accounts[platform]["user"],
                password=accounts[platform]["password"],
            )
        else:
            logger.error(
                f"{platform} 当前还不支持该平台, 请联系微信 Yida_Zhang2"
            )

    def _init_futures(self, accounts, trade_opts):
        from qbot.engine.trade.engine_apis.futures.futures_engine import (
            FuturesTradeEngine,
        )

        self.trade_engine = FuturesTradeEngine(
            accounts[trade_opts["platform"]], trade_opts, self.syslog
        )
        self.trade_engine.start_trade()
        if trade_opts["platform"] not in accounts:
            logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

    def _init_btc(self, accounts, trade_opts):
        from qbot.engine.trade.engine_apis.btc.btc_engine import BtcTradeEngine

        self.trade_engine = BtcTradeEngine(
            accounts[trade_opts["platform"]], trade_opts, self.syslog
        )
        self.trade_engine.start_trade()
        if trade_opts["platform"] not in accounts:
            logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

    def login(self):
        self.trade_engine.login()

    def get_cash(self):
        self.trade_engine.get_cash()

    def get_positions(self):
        self.trade_engine.get_positions()

    def load_strategy(self):
        pass

    def start_trade(self):
        self.trade_engine.start_trade()

    def close(self):
        self.trade_engine.close()
