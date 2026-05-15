# Qbot Backend Codebase Audit Report

**Date:** 2026-05-14
**Scope:** All Python files under `qbot/` excluding `qbot/gui/`
**Files Scanned:** ~180 Python files
**Auditor:** Automated scan + manual review

---

## Executive Summary

The Qbot backend codebase is a work-in-progress quantitative trading platform. Many strategies listed in the config are placeholder stubs with no implementation. Core trading engines have significant stub methods. Hardcoded API tokens and placeholder credentials are present in source code. The codebase has a mix of fully implemented strategies (backtrader-based) and many empty files or stubs.

**Total Findings: 72**
- HIGH: 16
- MEDIUM: 28
- LOW: 28

---

## HIGH Severity Findings

### H-01: Hardcoded Tushare API Token Exposed in Source Code
- **File:** `qbot/strategies/arbr_strategy.py`, line 33
- **Code:** `token = "6f747880359ef14fe2fd5fc0c2c08a4e09a47e7ac161d643ae7036c0"`
- **Impact:** API key committed to version control. This is a real Tushare Pro token that could be abused.
- **Fix:** Move to environment variable or secrets file. Rotate the token immediately.

### H-02: Hardcoded GMTrade Token and Account ID
- **File:** `qbot/engine/trade/engine_apis/stocks/gmtrade_example.py`, lines 22, 28
- **Code:** `set_token("c793349a885556506e27c2081c73091b4e77f28b")` and `account(account_id="5e4cdda3-f2fb-11ed-ae27-00163e022aa6")`
- **Impact:** Trading credentials exposed in version control. Could allow unauthorized trading.
- **Fix:** Move to secrets management. Rotate credentials.

### H-03: Multiple Strategy Files Listed in Config Are Completely Empty Stubs
- **Files:**
  - `qbot/strategies/bigger_than_ema.py` — empty (license header only)
  - `qbot/strategies/boll_strategy.py` — empty (license header + shebang only)
  - `qbot/strategies/boll_strategy_bt.py` — empty (shebang only)
  - `qbot/strategies/bigger_than_ema_test.py` — empty (shebang only)
- **Impact:** These strategies are listed as available options in `qbot/qbot.py` config but have zero implementation. Users selecting these strategies will get no functionality.
- **Note:** The backtrader versions (`bigger_than_ema_bt.py`) and (`boll_strategy_bt.py`) are implemented, but the base files referenced are empty.

### H-04: RL Strategy References Undefined `self.model`
- **File:** `qbot/strategies/rl_strategy_bt.py`, line 51
- **Code:** `action = self.model.predict(self.obs.reshape(1, -1))[0]`
- **Impact:** `self.model` is never assigned in `__init__`. This strategy will crash at runtime with `AttributeError`.
- **Note:** Also calls `self.log()` at line 60 but never defines a `log()` method (will crash in `stop()`).

### H-05: RL Strategy `__init__` Runs Full Training Before Backtest Data is Available
- **File:** `qbot/strategies/rl_strategy_bt.py`, line 44-45
- **Code:** `self.env = normalize(BacktraderEnv(self))` and `self.obs = self.env.reset()`
- **Impact:** The strategy attempts to create a BacktraderEnv from itself during `__init__`, before the Cerebro engine has set up data feeds. This will fail at runtime. The entire RL strategy is non-functional.

### H-06: BtcTradeEngine is Mostly Stub Pass Statements
- **File:** `qbot/engine/trade/engine_apis/btc/btc_engine.py`, lines 36-59
- **Code:** `start_trade()`, `get_balance()`, `get_all_tickers()`, `get_order_book()`, `get_account()`, `get_asset_balance()`, `order_market_buy()` — all contain only `pass`.
- **Impact:** Core BTC trading engine has no implementation. Only `login()` and `get_positions()` have partial logic.

### H-07: FuturesTradeEngine is a Complete Stub
- **File:** `qbot/engine/trade/engine_apis/futures/futures_engine.py`, line 13
- **Code:** `start_trade()` only does `pass`.
- **Impact:** Futures trading has zero implementation despite being listed as a supported trade type.

### H-08: OkxTradeEngine References Undefined Variables
- **File:** `qbot/engine/trade/engine_apis/btc/btc_trade_engine.py`, lines 131, 134, 137, 201, 207, 211
- **Code:** Uses `self.api_secret`, `self.api_key`, `self.passphrase`, `base_url`, `price` without `self.` prefix.
- **Impact:** `place_order()` at line 201 references `base_url` (should be `self.base_url`) and `price` (undefined variable). `get_headers()` references `self.api_secret` and `self.api_key` but these are set as local variables in `__init__`, not instance attributes. These methods will crash at runtime.

### H-09: HuobiTradeEngine Uses Binance Client (Copy-Paste Bug)
- **File:** `qbot/engine/trade/engine_apis/btc/btc_trade_engine.py`, lines 237-309
- **Code:** `HuobiTradeEngine.__init__` imports `from binance.client import Client` and creates a Binance client.
- **Impact:** Huobi trading engine is actually connecting to Binance API. Complete copy-paste error. Additionally, `order_limit_sell` at line 295 still references `self.client.order_limit_sell` (Binance method).

### H-10: CcxtTradeEngine.execute_trade Uses Undefined `exchange` (Missing `self.`)
- **File:** `qbot/engine/trade/engine_apis/btc/btc_trade_engine.py`, line 482
- **Code:** `ticker = exchange.fetch_ticker(symbol)` should be `self.exchange.fetch_ticker(symbol)`
- **Impact:** Will crash with `NameError` at runtime when stop-loss/take-profit logic triggers.

### H-11: `trade_engine.py` Has Redundant `pass` After Method Calls
- **File:** `qbot/engine/trade/trade_engine.py`, lines 37, 46, 51, 56
- **Code:** Methods like `login()`, `load_strategy()`, `start_trade()`, `close()` have unreachable `pass` after return-value calls or other statements.
- **Impact:** Code quality issue, but `load_strategy()` at line 46 is a stub (only `pass`), meaning strategy loading is not implemented.

### H-12: `load_strategy()` is a Stub Everywhere
- **Files:**
  - `qbot/engine/trade/trade_engine.py`, line 46 — `pass`
  - `qbot/engine/trade/trade_real.py`, line 140 — `pass`
  - `qbot/engine/trade/trade_sim.py`, line 142 — `pass`
  - `qbot/engine/trade/engine_apis/stocks/stock_engine.py`, line 33 — `pass`
- **Impact:** Strategy loading/plugging into the trade engine is not implemented. The trade engine cannot execute any strategy.

### H-13: EastmoneyTrader Uses Undefined `get_cash()` and `get_positions()`
- **File:** `qbot/engine/trade/engine_apis/stocks/stock_engine.py`, lines 160-168
- **Code:** `EastmoneyTrader.get_balance()` calls `get_cash()` and `EastmoneyTrader.get_positions()` calls `get_positions()` (both undefined globals, likely intended to be from gmtrade).
- **Impact:** EastmoneyTrader will crash when trying to get balance or positions.

### H-14: Bitcoin-Arbitrage Private Markets Have No Real Implementation
- **File:** `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/private_markets/market.py`
- **Code:** `buy()`, `sell()`, `balance()`, `withdraw()`, `deposit()` — all raise `NotImplementedError`.
- **Impact:** The bitcoin arbitrage system cannot execute any trades. The entire private_markets module is non-functional.

### H-15: Missing `qbot.engine.tokens` Module — Trade Engines Will Fail on Import
- **Files:**
  - `qbot/engine/trade/engine_apis/stocks/stock_engine.py`, line 50: `from qbot.engine.tokens import GMTRADE_ACCOUNT, GMTRADE_TOKEN`
  - `qbot/engine/backtest/live_trade_binance.py`, line 6: `from qbot.engine.tokens import binance_api`
- **Code:** No `tokens.py` file exists anywhere under `qbot/engine/`.
- **Impact:** Both `stock_engine.py` and `live_trade_binance.py` will crash with `ModuleNotFoundError` on import. This means the entire stock trading engine and Binance live trading are non-functional.

### H-16: Trade Platform Config Files Contain Plaintext Credentials
- **File:** `qbot/common/configs/trade_plat_para.json`
- **Code:** Multiple entries like `"user": "华泰证券用户名", "password": "华泰证券明文密码"` across all 13 broker entries.
- **Impact:** While these are placeholders, the JSON structure stores passwords in plaintext. When real credentials are added, they will be committed to version control. Also: Huobi `uid: "443400068"` appears to be a real user ID (line 76 of `btc_trade_plat_para.json`).

---

## MEDIUM Severity Findings

### M-01: Many Strategies Listed in Config Are "Reserved" (Not Implemented)
- **File:** `qbot/qbot.py`, lines 4-27
- **Details:** At least 17 of 28 listed strategies are marked as "预留" (reserved), meaning they have no implementation:
  - StochRSI, RSRS, MACD+ADX, Bollinger, Aroon, SMA, ARBR, Undervalued, SSA, SVM, LSTM, LGBM, Random Forest, Linear Regression, RL, Q-Learning, Turtle, Grid, Pair Trading, Kurtosis Portfolio, Multi-factor (several)
- **Impact:** Users see these as available options but they are non-functional.
- **Note:** Some like ARBR, LSTM, RSI, SMA, EMA, Boll, SSA, RL, Multi-strategy do have partial or full implementations in separate files, but they are not wired to the config system.

### M-02: `qbot/qbot.py` is a Standalone Script, Not a Module Entry Point
- **File:** `qbot/qbot.py`
- **Code:** Hardcoded `code = '601318'`, calls `get_data("600018")` at module level (line 39).
- **Impact:** Importing this module triggers side effects (API calls). It's a demo script, not the main application entry point.

### M-03: Amberdata API Key is Placeholder
- **File:** `qbot/engine/backtest/bitcoin_bt_example.py`, line 18
- **Code:** `Amberdata_API_KEY = "YOUR_API_KEY"`
- **Impact:** Bitcoin backtest example cannot run without replacing this key.

### M-04: Auto Monitor Token Placeholder
- **File:** `qbot/plugins/auto_monitor.py`, line 74
- **Code:** `pro = ts.pro_api("your token")`
- **Impact:** Monitor cannot fetch data without configuring a real token.

### M-05: `get_stack_data.py` Token Placeholder
- **File:** `qbot/strategies/get_stack_data.py`, line 26
- **Code:** `token='输入你自己的token'`
- **Impact:** `get_from_tushare_pro()` cannot work without real token.

### M-06: EasyTrader Example Has Placeholder Credentials
- **File:** `qbot/engine/trade/engine_apis/stocks/easytrader_example.py`, line 51
- **Code:** `username="your_username", password="your_password"`
- **Impact:** Cannot run without real credentials.

### M-07: Undervalued Stock Picking Strategy Depends on JoinQuant API
- **File:** `qbot/strategies/undervalued_stock_picking_strategy.py`
- **Code:** Uses `get_index_stocks()`, `get_fundamentals()`, `query()`, `set_benchmark()`, `run_monthly()` — all JoinQuant platform APIs.
- **Impact:** This strategy cannot run outside of the JoinQuant platform. It's not a standalone Python strategy.

### M-08: RSRS Strategy Has Undefined Variable Bug
- **File:** `qbot/engine/backtest/rsrs.py`, line 148
- **Code:** `timing_signal = self.get_timing_signal(stock_code)` — `stock_code` is undefined in `run()`.
- **Impact:** Will crash with `NameError` when `run()` is called.

### M-09: RSRS Strategy Uses Global Variable
- **File:** `qbot/engine/backtest/rsrs.py`, line 133
- **Code:** `global RSRS` inside a method
- **Impact:** Poor design pattern; makes the strategy non-reentrant and hard to test.

### M-10: `rsi_strategy_bt.py` Has No `__main__` Block or Data Loading
- **File:** `qbot/strategies/rsi_strategy_bt.py`
- **Code:** Defines `RSIStrategy` class but has no data source, no `__main__` block, no way to run standalone.
- **Impact:** Strategy exists but cannot be independently tested or executed.

### M-11: `rl_strategy_bt.py` Missing `model` Attribute Training
- **File:** `qbot/strategies/rl_strategy_bt.py`
- **Code:** `self.model` is used at line 51 but never defined. The RL strategy requires a trained model but has no training logic.
- **Impact:** Strategy is completely non-functional.

### M-12: `lstm_strategy_bt.py` Trains on Every Backtest Run
- **File:** `qbot/strategies/lstm_strategy_bt.py`, lines 46-47
- **Code:** Model is built and trained (50 epochs) inside `__init__` of the strategy.
- **Impact:** Extremely slow. Every time backtrader initializes the strategy, it retrains from scratch. Should train once and load saved weights.

### M-13: `multi_strategy_bt.py` and `sma_cross_strategy_bt.py` Execute Code at Module Level
- **Files:**
  - `qbot/strategies/multi_strategy_bt.py`, line 107: `dataframe = get_data("600018")`
  - `qbot/strategies/sma_cross_strategy_bt.py`, lines 82-83: `dataframe = get_data(...)` then `start = datetime(...)` outside `__main__`
- **Impact:** Importing these modules triggers tushare API calls. Will fail if tushare is not installed or returns errors.

### M-14: `bigger_than_ema_bt.py` and `lstm_strategy_bt.py` Also Execute at Module Level
- **Files:**
  - `qbot/strategies/bigger_than_ema_bt.py`, line 130: `dataframe = get_data("600018")`
  - `qbot/strategies/lstm_strategy_bt.py`, line 104: `dataframe = get_data("600018")`
- **Impact:** Same as M-13. Side effects on import.

### M-15: `auto_monitor.py` Runs Infinite Loop at Module Level
- **File:** `qbot/plugins/auto_monitor.py`, line 123
- **Code:** `while True:` loop with `time.sleep(2)` at module level.
- **Impact:** Importing this module will block forever.

### M-16: Duplicate Logger Implementations
- **Files:**
  - `qbot/common/logging/logger.py`
  - `qbot/common/logging/utils.py`
- **Impact:** Two separate logger classes with nearly identical code. The one in `utils.py` adds a `check_port_in_use()` function. Both create file handlers. Confusing which to use.

### M-17: Logger Uses Deprecated `warn()` Method
- **Files:**
  - `qbot/common/logging/logger.py`, line 29
  - `qbot/common/logging/utils.py`, line 29
  - `qbot/engine/trade/engine_apis/stocks/stock_engine.py`, line 15: `logger.warnning` (typo)
- **Impact:** `logger.warn()` is deprecated in Python 3.3+. Should use `logger.warning()`. The typo `warnning` will crash at runtime.

### M-18: `k_lines.py` Depends on Deprecated `mpl_finance`
- **File:** `qbot/strategies/k_lines.py`, line 19
- **Code:** `import mpl_finance as mpf`
- **Impact:** `mpl_finance` is deprecated and removed from matplotlib. Requires `mplfinance` package instead.

### M-19: `DumpDataBase.dump()` Raises NotImplementedError (Abstract)
- **File:** `qbot/data/dump_bin.py`, line 306
- **Code:** `raise NotImplementedError("dump not implemented!")`
- **Impact:** This is correct abstract method design (concrete implementations `DumpDataAll`, `DumpDataFix`, `DumpDataUpdate` exist), but the error message is misleading.

### M-20: `dump_pit.py` Has TODO for Missing PIT Database Design
- **File:** `qbot/data/dump_pit.py`, lines 4-7
- **Code:** `TODO: A more well-designed PIT database is required. - separated insert, delete, update, query operations are required.`
- **Impact:** PIT data functionality is incomplete.

### M-21: `dagster_taskgraph.py` Has Hardcoded Test Data
- **File:** `qbot/plugins/dagster/dagster_taskgraph.py`, line 15
- **Code:** `items = ["1", "2", "3"]` overwriting database query results
- **Impact:** Dagster pipeline always processes hardcoded items, not real data.

### M-22: `rsi_strategy_bt.py` RSI Thresholds Differ from Docstring
- **File:** `qbot/strategies/rsi_strategy_bt.py`, lines 11-12
- **Code:** Docstring says "Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought)" but defaults are `rsi_lower=40, rsi_upper=60`.
- **Impact:** Misleading documentation. Strategy behavior doesn't match description.

### M-23: `config.py` Uses `ASSERTS_DIR` (Typo for `ASSETS_DIR`)
- **File:** `qbot/engine/config.py`, line 22
- **Code:** `ASSERTS_DIR = Path(__file__).parent.parent.parent.joinpath("asserts")`
- **Impact:** Typo in directory name. Also the path uses `asserts` (not `assets`). If the actual directory is named `assets`, this path is wrong.

### M-24: `qbot.py` Config Missing Comma Creates String Concatenation Bug
- **File:** `qbot/qbot.py`, lines 38-39
- **Code:** `"海通证券"` followed by `"国金证券"` with no comma between them
- **Impact:** Python string concatenation: `"海通证券国金证券"` — creates a single invalid platform name. Also `"银河证券"` appears twice (lines 41 and 43).

### M-25: `rl_strategy_bt.py` Imports Expensive Libraries That Are Never Used
- **File:** `qbot/strategies/rl_strategy_bt.py`, lines 32-36
- **Code:** `from keras.models import Sequential`, `from keras.layers import Dense, LSTM, Dropout`, `from sklearn.preprocessing import MinMaxScaler`, `from rlkit.envs.backtrader_env import BacktraderEnv`, `from rlkit.envs.normalized_env import normalize`
- **Impact:** Four heavy ML libraries imported but never actually used (model is never created, scaler never used). keras/tensorflow alone adds ~500MB to memory on import. The `rlkit` library is likely not even installed in most environments.
- **Note:** `rlkit` is not a standard pip package — it requires manual installation from a specific GitHub repo.

### M-26: `rsrs.py` Imports Expensive JoinQuant SDK for a Single Script
- **File:** `qbot/engine/backtest/rsrs.py`, line 14
- **Code:** `import jqdatasdk as jq`
- **Impact:** JoinQuant SDK requires authentication and is only usable on the JoinQuant platform. The entire `rsrs.py` file cannot run outside that environment. Also imports `easyquant.quotation` (line 3) which is an obscure package.

### M-27: `auto_monitor.py` References Non-Existent Module Path
- **File:** `qbot/plugins/auto_monitor.py`, line 32
- **Code:** `from utils.larkbot import LarkBot`
- **Impact:** `utils.larkbot` is found at `/Users/harshai/Documents/Qbot/utils/larkbot.py` (project root), not as a proper Python package. This import will fail when running from any directory other than the project root. Should be a proper package under `qbot/`.

### M-28: `bitcoin-arbitrage/__init__.py` Executes Code on Import
- **File:** `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/__init__.py`
- **Code:** `from arbitrage import arbitrage` then `arbitrage.main()`
- **Impact:** Simply importing this package triggers the main arbitrage loop. This is a serious side-effect-on-import issue.

---

## LOW Severity Findings

### L-01: Bare `except:` Clauses (Silently Swallowing Errors)
- **Files and lines:**
  - `qbot/engine/trade/easytrader/easytrader/joinquant_follower.py`, line 68: `except:`
  - `qbot/engine/trade/easytrader/easytrader/clienttrader.py`, lines 278, 484: `except:`
  - `qbot/engine/trade/easytrader/easytrader/universal_clienttrader.py`, line 41: `except:`
  - `qbot/engine/trade/easytrader/easytrader/grid_strategies.py`, lines 67, 94: `except:`
  - `qbot/plugins/auto_monitor.py`, line 77: `except: # noqa E722`
- **Impact:** Errors are silently caught with no logging. Makes debugging very difficult.

### L-02: `get_stack_data.py` Imports Same Module Multiple Times
- **File:** `qbot/strategies/get_stack_data.py`, lines 17, 25, 45, 57
- **Code:** `import tushare as ts` appears twice (lines 17 and 25)
- **Impact:** Unnecessary duplicate import. Code quality issue.

### L-03: `arbr_strategy.py` Has Unused Import
- **File:** `qbot/strategies/arbr_strategy.py`, line 15
- **Code:** `import numpy as np  # noqa F401`
- **Impact:** `numpy` is imported but never used.

### L-04: `auto_monitor.py` Has Unused Import
- **File:** `qbot/plugins/auto_monitor.py`, line 23
- **Code:** `import urllib.request  # noqa F401`
- **Impact:** Never used.

### L-05: `dagster_taskgraph.py` Has Unused Imports
- **File:** `qbot/plugins/dagster/dagster_taskgraph.py`, lines 3-4
- **Code:** `from dagster import asset` and `from dagster import get_dagster_logger`
- **Impact:** Never used.

### L-06: `rl_strategy_bt.py` Has Unused Imports
- **File:** `qbot/strategies/rl_strategy_bt.py`, lines 33-34
- **Code:** `from keras.models import Sequential` and `from keras.layers import Dense, LSTM, Dropout`
- **Impact:** Imported but never used (model is never created).

### L-07: `rsa_strategy.py` Has Inconsistent Return from `get_ols()`
- **File:** `qbot/engine/backtest/rsrs.py`, lines 49-58
- **Code:** `get_ols()` can return `None` if exception is caught, but callers assume a tuple is returned.
- **Impact:** Will crash downstream when trying to index `None`.

### L-08: `util.py` References `np` Without Import
- **File:** `qbot/strategies/util.py`, line 58
- **Code:** `nanCounter = np.count_nonzero(...)` but `numpy` is never imported.
- **Impact:** Will crash with `NameError`.

### L-09: `rsrs.py` `get_ols()` Silent Error Swallowing
- **File:** `qbot/engine/backtest/rsrs.py`, line 57-58
- **Code:** `except Exception as e: print(e)` — returns `None` implicitly.
- **Impact:** Callers get `None` and crash when unpacking.

### L-10: `easytrader_example.py` Has Infinite Loop
- **File:** `qbot/engine/trade/engine_apis/stocks/easytrader_example.py`, line 59
- **Code:** `while True: strategy.execute()` — no exit condition.
- **Impact:** Example will run forever if executed.

### L-11: `backtest_base.py` Template Methods Return Hardcoded 0
- **File:** `qbot/engine/backtest/backtest_base.py`, lines 51-54
- **Code:** `get_singal()` returns `0`, `get_scores()` returns `0`.
- **Impact:** Base template always signals "hold". This is by design (template pattern) but undocumented.

### L-12: `bitfinex`, `bitflyer` Public Markets Silently Catch All Exceptions
- **Files:**
  - `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_bitfinex.py`, line 21
  - `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_bitflyer.py`, line 46
- **Code:** `except Exception:` with `pass`
- **Impact:** Network errors and data issues are silently ignored.

### L-13: `bitcoin_bt_example.py` `notify_order` Has Empty Completed Block
- **File:** `qbot/engine/backtest/bitcoin_bt_example.py`, line 127
- **Code:** `if order.status == order.Completed: pass`
- **Impact:** Completed orders are not logged or handled.

### L-14: Missing `__init__.py` in `qbot/engine/trade/engine_apis/btc/`
- **Impact:** Cannot import the btc engine package as a Python package (relative imports may fail).

### L-15: `setup.py` Entry Point is Incorrect
- **File:** `qbot/setup.py`, line 67
- **Code:** `'sample=sample:main'` — references a non-existent `sample` module.
- **Impact:** `pip install` creates a broken `sample` CLI command.

### L-16: `stock_engine.py` Missing Semicolon Bug in `if` Chain
- **File:** `qbot/engine/trade/engine_apis/stocks/stock_engine.py`, line 36-43
- **Code:** The `CcxtTradeEngine` block uses `if` for "币安Binance" (line 321) instead of `elif`, meaning two `if` blocks are checked even when the first matches.
- **Impact:** Not a bug per se (second block would also match for Binance), but indicates a likely typo.

### L-17: `trader/utils/read_config.py` Has Hardcoded Test Token
- **File:** `qbot/engine/trade/trader/trader/utils/read_config.py`, line 54
- **Code:** `token = 123456`
- **Impact:** Test credential in source code.

### L-18: `FuturesTradeEngine.__main__` References `self` Outside Class
- **File:** `qbot/engine/trade/engine_apis/futures/futures_engine.py`, line 24
- **Code:** `futures_engine = FuturesTradeEngine(trade_opts["platform"], trade_opts, self.syslog)` — `self` is not defined in module scope.
- **Impact:** Will crash with `NameError` if run as script.

### L-19: `trade_sim.py` and `trade_real.py` Reference Undefined `accounts` Variable
- **Files:**
  - `qbot/engine/trade/trade_sim.py`, line 49: `password=accounts["华泰证券"]["password"]` — but variable is `sim_accounts`
  - `qbot/engine/trade/trade_real.py`, line 159: `SimTradeEngine` used instead of `RealTradeEngine`; line 169: `sim_accounts` used but `real_accounts` is the intended variable
- **Impact:** Will crash with `NameError` if those code paths are reached.

### L-20: `btc_engine.py` References Undefined `logger` in `__main__`
- **File:** `qbot/engine/trade/engine_apis/btc/btc_engine.py`, line 88
- **Code:** `logger.error(...)` — `logger` is not imported in this file (uses `LOGGER` import pattern from other files, but this file doesn't import it).
- **Impact:** Will crash with `NameError` in `__main__` block.

### L-21: `back_para.json` Has Hardcoded Backtest Parameters
- **File:** `qbot/common/configs/back_para.json`, lines 39-43
- **Code:** `"cash_hold": "100000"`, `"slippage": "0.01"`, `"c_rate": "0.0005"`, `"t_rate": "0.001"`, `"stake_size": "all"`
- **Impact:** Backtesting parameters are hardcoded in a JSON config file. Values are stored as strings instead of numbers. These are not "results" per se, but they are not dynamically configurable by the user.

### L-22: `firm_para.json` Has Hardcoded Title "000651 格力电器-日K线"
- **File:** `qbot/common/configs/firm_para.json`, line 37
- **Code:** `"title": "000651 格力电器-日K线"`
- **Impact:** Chart title is hardcoded for a specific stock. Not dynamically generated.

### L-23: `btc_trade_plat_para.json` Contains VIP Referral Link
- **File:** `qbot/common/configs/btc_trade_plat_para.json`, line 33
- **Code:** `"vip_channel": "https://www.cnouyi.social/join/57246734"`
- **Impact:** Contains an OKX referral/affiliate link in the config. This is a monetization feature embedded in what appears to be an open-source project config.

### L-24: `investool` Plugin is Go, Not Python
- **Path:** `qbot/plugins/investool/`
- **Impact:** The investool plugin is written in Go (main.go, core/*.go, etc.) with its own config.toml. It has its own web server, CI/CD, and dependency management. It's a separate project embedded in the Qbot repo, adding complexity.

### L-25: `investool/config.toml` Has Default Admin Credentials
- **File:** `qbot/plugins/investool/config.toml`, lines 142-143
- **Code:** `username = "admin"`, `password = "admin"`
- **Impact:** Default credentials for the investool web server.

### L-26: `sys_para.json` Contains License Management Fields
- **File:** `qbot/common/configs/sys_para.json`, lines 22-27
- **Code:** `"license_reminder_box": {"latest_pop_date": "20240831", "release_date": "20230829", "license_created": false}`
- **Impact:** The project has license/reminder infrastructure. `license_created: false` suggests licensing is not active, but the framework exists.

### L-27: `trade_plat_para.json` References VIP in Ads
- **File:** `qbot/common/configs/trade_plat_para.json`, line 159
- **Code:** `"'开户VIP超低佣金'"`
- **Impact:** Broker promotional text with VIP language embedded in config.

### L-28: `rsrs.py` Function Named `get_payments` is Actually a Backtest Runner
- **File:** `qbot/engine/backtest/rsrs.py`, line 164
- **Code:** `def get_payments(...)` — function name suggests payment-related but it actually runs RSRS backtesting and computes strategy returns.
- **Impact:** Misleading function name. Should be renamed to something like `run_rsrs_backtest()`.

---

## Strategy Implementation Summary

| Strategy | File | Status | Data Source | Configurable? |
|----------|------|--------|-------------|---------------|
| RSI | `rsi_strategy_bt.py` | Implemented (no runner) | None (needs data feed) | Params: period, thresholds |
| SMA Cross | `sma_cross_strategy_bt.py` | Implemented | Tushare (hardcoded) | Params: fast, slow |
| EMA Bigger | `bigger_than_ema_bt.py` | Implemented | Tushare (hardcoded) | Params: period |
| Bollinger | `boll_strategy_bt.py` | Implemented | AKShare | Params: nk period |
| Multi (RSI+SMA) | `multi_strategy_bt.py` | Implemented | Tushare (hardcoded) | Params: exitbars, period |
| LSTM | `lstm_strategy_bt.py` | Partial (retrains on init) | Tushare (hardcoded) | Params: period, neurons, lookback |
| RL | `rl_strategy_bt.py` | **Broken** (no model) | Tushare (hardcoded) | N/A |
| SSA | `ssa_strategy_bt.py` | Implemented | Local CSV file | Params: ssa_window, period |
| ARBR | `arbr_strategy.py` | Implemented | Tushare Pro (hardcoded token) | Hardcoded params |
| ADX+MACD | `adx_strategy.py` | Implemented | Tushare (hardcoded) | Hardcoded params |
| K-Lines | `k_lines_bt.py` | Implemented | efinance | Hardcoded params |
| RSRS | `rsrs.py` | **Bug** (undefined var) | JoinQuant | Hardcoded params |
| Undervalued | `undervalued_stock_picking_strategy.py` | JoinQuant-only | JoinQuant platform | Hardcoded params |
| MACD BT | `macd_bt.py` | Implemented | Tushare (hardcoded) | Hardcoded params |
| Bitcoin BT | `bitcoin_bt_example.py` | Needs API key | Amberdata | Hardcoded params |
| Binance Live | `live_trade_binance.py` | Needs API key | Binance | Hardcoded params |

---

## Recommendations (Prioritized)

1. **CRITICAL:** Remove hardcoded API tokens (`arbr_strategy.py:33`, `gmtrade_example.py:22,28`). Rotate all exposed credentials immediately.

2. **CRITICAL:** Fix `rl_strategy_bt.py` — either implement model loading/training or mark as not functional.

3. **CRITICAL:** Create the missing `qbot/engine/tokens.py` module or refactor imports. Currently `stock_engine.py` and `live_trade_binance.py` will crash on import.

4. **HIGH:** Fix `btc_trade_engine.py` — OkxTradeEngine undefined variables, HuobiTradeEngine copy-paste bug, CcxtTradeEngine `exchange` reference.

5. **HIGH:** Implement `load_strategy()` or remove references to it across all trade engines.

6. **HIGH:** Fix module-level side effects in strategy files (`multi_strategy_bt.py`, `sma_cross_strategy_bt.py`, `lstm_strategy_bt.py`, `bigger_than_ema_bt.py`, `auto_monitor.py`, `bitcoin-arbitrage/__init__.py`).

7. **MEDIUM:** Move all strategy data fetching and backtest execution into `__main__` blocks.

8. **MEDIUM:** Clean up the strategy config (`qbot/qbot.py`) to only list actually implemented strategies, or clearly mark unimplemented ones.

9. **MEDIUM:** Fix the string concatenation bug in trade platforms list (`qbot/qbot.py:38`).

10. **MEDIUM:** Remove unused expensive imports from `rl_strategy_bt.py` (keras, sklearn, rlkit) or implement the strategy properly.

11. **MEDIUM:** Move credential storage from JSON config files to environment variables or a secrets manager. Current JSON structure stores passwords in plaintext.

12. **LOW:** Replace bare `except:` with proper exception handling and logging.

13. **LOW:** Fix `setup.py` entry point from `sample` to a real module.

14. **LOW:** Remove dead/unused imports across the codebase (`numpy` in arbr, `urllib` in auto_monitor, `asset`/`get_dagster_logger` in dagster).
