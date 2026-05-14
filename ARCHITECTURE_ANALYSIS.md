# Qbot Codebase Architecture Analysis

> **Project:** UFund-Me/Qbot — AI智能量化投研平台 (AI Quantitative Trading Research Platform)  
> **Author:** Charmve (yidazhang1@gmail.com)  
> **Version:** 1.0.1  
> **License:** MIT  
> **Analysis Date:** 2026-05-13  

---

## Table of Contents

1. [Project Structure Overview](#1-project-structure-overview)
2. [Entry Points & Boot Sequence](#2-entry-points--boot-sequence)
3. [GUI Framework Architecture](#3-gui-framework-architecture)
4. [Module Architecture & Dependency Graph](#4-module-architecture--dependency-graph)
5. [Stub Functions Inventory (Critical)](#5-stub-functions-inventory-critical)
6. [Data Flow Analysis](#6-data-flow-analysis)
7. [Backend / Engine Components](#7-backend--engine-components)
8. [Strategy Framework](#8-strategy-framework)
9. [Extensibility Assessment](#9-extensibility-assessment)
10. [Third-Party Dependencies](#10-third-party-dependencies)
11. [Key Findings & Recommendations](#11-key-findings--recommendations)

---

## 1. Project Structure Overview

```
Qbot/
├── main.py                          # Primary entry point (wxPython GUI app)
├── qbot_main.py                     # Secondary CLI entry point (tushare + talib)
├── requirements.txt                 # Python dependencies
├── env_setup.sh                     # Environment setup script
├── monitoring.py                    # Monitoring utility
├── WORKSPACE                        # Bazel workspace config
│
├── qbot/                            # === CORE APPLICATION PACKAGE ===
│   ├── qbot.py                      # Core Qbot class (tushare, talib)
│   ├── version.py                   # Version: "0.1.1"
│   │
│   ├── common/                      # Shared utilities & configuration
│   │   ├── config.py                # Path constants (duplicate of engine/config.py)
│   │   ├── macros.py                # Strategy choices, trade platform lists
│   │   ├── file_utils.py            # JSON/CSV file I/O helpers
│   │   ├── utils.py                 # Logger class, port checker
│   │   ├── logging/                 # Logging module
│   │   │   ├── logger.py            # LOGGER singleton
│   │   │   └── utils.py
│   │   └── configs/                 # JSON config files
│   │       ├── sys_para.json        # System parameters
│   │       ├── firm_para.json       # Firm parameters
│   │       ├── back_para.json       # Backtest parameters
│   │       ├── trade_plat_para.json # Stock trade platform config
│   │       └── btc_trade_plat_para.json # BTC trade platform config
│   │
│   ├── gui/                         # GUI layer (wxPython)
│   │   ├── gui_utils.py             # wx.DateTime ↔ Python datetime converters
│   │   ├── config.py                # GUI-specific path constants
│   │   ├── mainframe.py             # MainFrame — top-level window
│   │   ├── panels/                  # Tab panels
│   │   │   ├── panel_backtest.py    # Backtest panel
│   │   │   ├── panel_trade.py       # Trade tab container (sim + real)
│   │   │   ├── panel_sim_trade.py   # Simulated trading panel
│   │   │   ├── panel_real_trade.py  # Real trading panel
│   │   │   ├── panel_results.py     # Results visualization panel
│   │   │   └── panel_zhiku.py       # "智库" (knowledge) panel
│   │   ├── elements/                # Reusable GUI elements
│   │   │   ├── def_dialog.py        # Dialog boxes (Message, User, Params, Web)
│   │   │   ├── def_grid.py          # GridTable (wx.grid.Grid wrapper)
│   │   │   └── def_treelist.py      # TreeListCtrl for strategy navigation
│   │   ├── widgets/                 # Embeddable widgets
│   │   │   ├── widget_web.py        # WebPanel (wx.html2.WebView wrapper)
│   │   │   └── widget_matplotlib.py # MatplotlibPanel (matplotlib in wx)
│   │   ├── common/                  # GUI-specific utilities
│   │   │   ├── SysFile.py           # File operations (JSON, CSV, log)
│   │   │   └── PrintLog.py          # SysLogIf — log text widget interface
│   │   └── imgs/                    # Icons and images
│   │       └── logo.ico
│   │
│   ├── engine/                      # Backend engine
│   │   ├── config.py                # Path constants (data dirs, account files)
│   │   ├── tokens.py                # API tokens (MISSING — referenced but absent)
│   │   ├── backtest/                # Backtesting framework
│   │   │   ├── backtest_base.py     # BacktestStrategyTemplate base class
│   │   │   ├── backtest_main.py     # Backtest runner (uses JoinQuant + RSI)
│   │   │   ├── bitcoin_bt_example.py
│   │   │   ├── live_trade_binance.py
│   │   │   ├── macd_bt.py
│   │   │   └── rsrs.py
│   │   └── trade/                   # Trading execution
│   │       ├── trade_engine.py      # TradeEngine — facade for sim/real
│   │       ├── trade_sim.py         # SimTradeEngine
│   │       ├── trade_real.py        # RealTradeEngine
│   │       ├── engine_apis/         # Platform-specific implementations
│   │       │   ├── stocks/          # Stock trading (掘金, 东方财富, easytrader)
│   │       │   │   └── stock_engine.py
│   │       │   ├── btc/             # Crypto trading (OKX, Binance, ccxt)
│   │       │   │   ├── btc_engine.py
│   │       │   │   └── btc_trade_engine.py
│   │       │   ├── futures/         # Futures trading (CTP) — STUB
│   │       │   │   └── futures_engine.py
│   │       │   ├── funds/           # Fund trading — EMPTY (account.json only)
│   │       │   └── options/         # Options trading — EMPTY (account.json only)
│   │       ├── easytrader/          # Bundled easytrader library
│   │       ├── trader/              # CTP-based futures trader (Django app)
│   │       └── trading/             # Additional trading sub-projects
│   │           ├── bitcoin-arbitrage/   # BTC arbitrage engine
│   │           ├── emt_api/             # EMT (Emergent Trading) API
│   │           └── thsauto/             # 同花顺 auto-trading
│   │
│   ├── strategies/                  # Trading strategy implementations
│   │   ├── boll_strategy_bt.py      # Bollinger Bands (backtrader)
│   │   ├── boll_strategy.py         # Bollinger Bands (empty file)
│   │   ├── sma_cross_strategy_bt.py # SMA Crossover (backtrader)
│   │   ├── adx_strategy.py          # ADX indicator strategy
│   │   ├── arbr_strategy.py         # ARBR sentiment strategy
│   │   ├── bigger_than_ema_bt.py    # EMA strategy (backtrader)
│   │   ├── bigger_than_ema.py       # EMA strategy
│   │   ├── ssa_strategy_bt.py       # Sparrow Search Algorithm (ML)
│   │   ├── lstm_strategy_bt.py      # LSTM prediction (backtrader)
│   │   ├── rl_strategy_bt.py        # Reinforcement Learning (backtrader)
│   │   ├── multi_strategy_bt.py     # Multi-strategy (backtrader)
│   │   ├── klines_bt.py             # K-line analysis
│   │   ├── k_lines.py               # K-line utilities
│   │   ├── undervalued_stock_picking_strategy.py  # Value investing
│   │   ├── get_stack_data.py        # Data fetching helper
│   │   └── util.py                  # Strategy utilities
│   │
│   ├── plugins/                     # Plugin modules
│   │   ├── auto_monitor.py          # Automated monitoring
│   │   ├── quantstats/              # Bundled quantstats library
│   │   └── dagster/                 # Dagster task graph integration
│   │
│   └── asserts/                     # Static assets
│       └── statics/sounds/bell.wav  # Notification sound
│
├── pytrader/                        # Independent trading framework
│   ├── easyquant/                   # Quantitative trading engine
│   ├── easyquotation/               # Market data fetching
│   ├── easytrader/                  # Trade execution (broker adapters)
│   ├── strategies/                  # Strategy implementations
│   ├── analyser/                    # Performance analysis
│   ├── frontend/                    # Web frontend
│   └── web/                         # Web server
│
├── pyfunds/                         # Fund (mutual fund) trading
│   ├── backtest/                    # Fund backtesting
│   ├── fund-strategies/             # Fund strategies
│   ├── coffeelings/                 # Fund analysis tool
│   └── web-extension/               # Browser extension
│
├── pyfutures/                       # Futures trading
│   ├── ctp/                         # CTP (Comprehensive Transaction Platform)
│   ├── futuresDemo.py               # Demo script
│   └── sma_cross_strategy_bt.py     # SMA strategy for futures
│
├── data/                            # Data storage (auto-created)
│   ├── stocks/                      # CSV stock data
│   ├── hdf5/                        # HDF5 format data
│   ├── futures/                     # Futures data
│   ├── funds/                       # Fund data
│   ├── btc/                         # BTC data
│   ├── options/                     # Options data
│   ├── multi-facts/                 # Multi-factor data
│   └── qlib_data/                   # Qlib data
│
├── results/                         # Results storage (auto-created)
│   ├── bkt_result/                  # Backtest results
│   ├── bk_result/                   # Backtest results (alternate)
│   ├── hdf5/                        # HDF5 results
│   └── indicators/                  # Indicator results
│
├── docs/                            # Documentation
│   ├── notebook/                    # Jupyter notebooks
│   └── research_reports/            # Research reports (PDFs)
│
├── dev/                             # Development scripts
└── utils/                           # Utility scripts
    └── configure/util.py            # Configuration utilities
```

---

## 2. Entry Points & Boot Sequence

### 2.1 Primary Entry: `main.py`

```
#!/usr/bin/python
```

**Boot sequence:**
1. Imports `wx` (wxPython)
2. Creates `wx.App()`
3. Instantiates `MainFrame(None, title="AI智能量化投研平台")`
4. Shows the frame, starts `app.MainLoop()`

This is a thin wrapper — all logic lives in `qbot/gui/mainframe.py`.

### 2.2 Secondary Entry: `qbot_main.py`

A CLI/alternative entry point that:
- Uses `tushare` for stock data
- Uses `talib` for technical analysis
- Loads a Keras/TensorFlow model
- Sends notifications via `LarkBot` (飞书) and `pync` (macOS notifications)
- Operates on stock code `'601318'` (中国平安)

### 2.3 Core Module: `qbot/qbot.py`

A standalone stock analysis script:
- Fetches data via `tushare`
- Computes technical indicators via `talib`
- Hardcoded to stock `'601318'`

---

## 3. GUI Framework Architecture

### 3.1 Framework: wxPython (wx)

The entire GUI is built on **wxPython** with embedded **wx.html2.WebView** for web content display.

### 3.2 MainFrame (`qbot/gui/mainframe.py`)

```
MainFrame(wx.Frame)
├── Menu Bar
│   ├── 主菜单
│   │   ├── 蛋卷估值  → opens web URL
│   │   ├── 集思录    → opens web URL
│   │   └── 后台监控  → opens web URL
│   └── 设置
│       └── 参数配置  → ParamsConfigDialog
│
├── Notebook (Tab Control)
│   ├── Tab 1: PanelBacktest       — "量化回测" (Quantitative Backtest)
│   ├── Tab 2: TradePanel          — "模拟交易 + 实盘交易" (Trading)
│   │   ├── SimTradePanel          — "模拟交易" (Simulated Trading)
│   │   └── RealTradePanel         — "实盘交易" (Real Trading)
│   ├── Tab 3: ZhikuPanel          — "量化智库" (Knowledge Hub)
│   │   ├── QbotHomePanel          — Qbot official website (WebView)
│   │   ├── YanbaoPanel            — Research reports viewer (PDF via HTTP)
│   │   └── NotebookPanel          — Jupyter notebook (WebView)
│   └── Tab 4: WebPanel            — "在线投研" (Web Research)
│
├── Status Bar (with version display)
└── Sound: bell.wav on events
```

### 3.3 Panel Architecture

#### PanelBacktest (`panel_backtest.py`)
- **Layout:** Horizontal split — parameter area (Notebook with "行情参数" and "回测参数" tabs) + WebView display
- **Parameters captured:** start/end time, stock code, period, benchmark, initial cash, stake, slippage, commission, stamp duty, strategy selection
- **Strategies offered:** 25 choices from `macros.strategy_choices` (most marked "预留" = reserved/stub)
- **Key issue:** Both `LoadData` and `StartBacktest` are **stubbed** — show WeChat contact dialog

#### SimTradePanel (`panel_sim_trade.py`)
- **Layout:** Complex multi-area layout — stock pool grid, stock list, trade log, parameter notebook, strategy tree, WebView
- **Parameters:** trade type (股票/期货/基金/BTC/期权), platform selection, strategy selection
- **Trade execution:** Creates `TradeEngine` with `trader_opts` dict, calls login → get_positions → start_trade
- **WebView:** Shows platform-specific trading interfaces (掘金 for stocks, OKX/Binance for crypto)
- **Partial functionality:** OnClickTrade actually instantiates TradeEngine (but defaults to hardcoded "东方财富" sim opts)

#### RealTradePanel (`panel_real_trade.py`)
- Nearly identical structure to SimTradePanel
- Trade engine initialized with `"class": "实盘"` instead of `"虚拟盘"`
- Same stub patterns

#### TradePanel (`panel_trade.py`)
- Simple container that creates a nested Notebook with SimTradePanel + RealTradePanel

#### ResultsPanel (`panel_results.py`)
- 8-tab notebook for displaying: raw data, K-line charts, Bollinger charts, feature extraction, plots, risk/reward, yearly returns, correlation analysis
- **Broken import:** `from qbot.gui.widgets.widgets import MatplotlibPanel, PandasGrid` — this module **does not exist**
- `PandasGrid` is likely defined somewhere but the import path is wrong

#### ZhikuPanel (`panel_zhiku.py`)
- 3-tab notebook: Qbot website (WebView), research reports (PDF served via local HTTP server on port 9080), Jupyter notebooks

### 3.4 GUI Elements

| Component | File | Purpose |
|-----------|------|---------|
| `MessageDialog` | `def_dialog.py` | wx.MessageDialog wrapper for Yes/No prompts |
| `ChoiceDialog` | `def_dialog.py` | wx.SingleChoiceDialog wrapper |
| `WebDialog` | `def_dialog.py` | wx.Dialog with embedded WebView |
| `UserDialog` | `def_dialog.py` | Displays trade log in read-only text |
| `InputsDialog` | `def_dialog.py` | Username/password input dialog |
| `InputDialogTwoParameters` | `def_dialog.py` | Generic two-parameter input |
| `ParamsConfigDialog` | `def_dialog.py` | Full parameter configuration (OS, data source, data store, trade platforms, display params, licensing) |
| `GridTable` | `def_grid.py` | wx.grid.Grid wrapper with auto-resize, DataFrame/dict loading |
| `CollegeTreeListCtrl` | `def_treelist.py` | Tree list for strategy navigation (经典策略, 自定义策略, 衍生指标, K线形态) |
| `WebPanel` | `widget_web.py` | wx.html2.WebView panel with show_url/show_file |
| `MatplotlibPanel` | `widget_matplotlib.py` | Matplotlib canvas in wx.ScrolledWindow |
| `SysLogIf` | `PrintLog.py` | TextCtrl log interface |
| `Base_File_Oper` | `SysFile.py` | JSON/CSV/txt file operations |

---

## 4. Module Architecture & Dependency Graph

### 4.1 Import Dependency Graph (Simplified)

```
main.py
  └── qbot.gui.mainframe.MainFrame
        ├── qbot.gui.panels.panel_backtest.PanelBacktest
        │     ├── qbot.common.macros.strategy_choices
        │     ├── qbot.common.file_utils.extract_content
        │     ├── qbot.gui.elements.def_dialog.MessageDialog
        │     └── qbot.gui.widgets.widget_web.WebPanel
        │
        ├── qbot.gui.panels.panel_trade.TradePanel
        │     ├── qbot.gui.panels.panel_sim_trade.SimTradePanel
        │     │     ├── qbot.common.macros (strategy_choices, trade_platforms, btc_*, futures_*)
        │     │     ├── qbot.engine.trade.trade_engine.TradeEngine
        │     │     ├── qbot.gui.elements.def_dialog (MessageDialog, UserDialog)
        │     │     ├── qbot.gui.elements.def_grid.GridTable
        │     │     ├── qbot.gui.elements.def_treelist.CollegeTreeListCtrl
        │     │     └── qbot.gui.widgets.widget_web.WebPanel
        │     │
        │     └── qbot.gui.panels.panel_real_trade.RealTradePanel
        │           └── (same imports as SimTradePanel)
        │
        ├── qbot.gui.panels.panel_zhiku.ZhikuPanel
        │     ├── qbot.common.config.RESEARCH_REPORTS
        │     ├── qbot.common.utils.check_port_in_use
        │     └── qbot.gui.widgets.widget_web.WebPanel
        │
        ├── qbot.gui.panels.panel_results.ResultsPanel
        │     ├── qbot.gui.widgets.widgets.MatplotlibPanel  ← MISSING MODULE
        │     └── qbot.gui.widgets.widgets.PandasGrid       ← MISSING MODULE
        │
        ├── qbot.gui.elements.def_dialog.ParamsConfigDialog
        │     └── qbot.gui.common.SysFile.Base_File_Oper
        │
        └── qbot.gui.widgets.widget_web.WebPanel

qbot.engine.trade.trade_engine.TradeEngine
  ├── qbot.engine.trade.trade_sim.SimTradeEngine
  │     ├── qbot.engine.trade.engine_apis.stocks.stock_engine.StockTradeEngine
  │     │     ├── GmSimTrader (掘金 quantitative platform)
  │     │     └── EastmoneyTrader (东方财富)
  │     ├── qbot.engine.trade.engine_apis.futures.futures_engine.FuturesTradeEngine
  │     ├── qbot.engine.trade.engine_apis.btc.btc_engine.BtcTradeEngine
  │     │     ├── BinanceTradeEngine (python-binance)
  │     │     ├── OkxTradeEngine (REST API + HMAC)
  │     │     └── CcxtTradeEngine (ccxt library, multi-exchange)
  │     └── easytrader (bundled: 同花顺, 华泰, 通达信, 银河, 雪球)
  │
  └── qbot.engine.trade.trade_real.RealTradeEngine
        └── (same platform hierarchy as SimTradeEngine)
```

### 4.2 Configuration Layer

Two config modules with **duplicated** path constants:
- `qbot/common/config.py` — used by `panel_zhiku.py`, strategies
- `qbot/engine/config.py` — used by `trade_sim.py`, `trade_real.py`, `stock_engine.py`

Both define identical constants: `DATA_DIR`, `RESULT_DIR`, `STOCK_SIM_ACCOUNT`, etc.

### 4.3 Token Management

`qbot/engine/tokens.py` is **referenced** (imported as `from qbot.engine.tokens import GMTRADE_ACCOUNT, GMTRADE_TOKEN, binance_api`) but **does not exist** on disk. This is a critical missing file that would contain:
- 掘金 (MyQuant) API token & account ID
- Binance API credentials
- Other platform tokens

---

## 5. Stub Functions Inventory (Critical)

### 5.1 GUI-Level Stubs (Paywall Dialogs)

These functions display a dialog asking users to contact WeChat ID `Yida_Zhang2`:

| File | Line | Function | Intended Purpose | Stub Behavior |
|------|------|----------|------------------|---------------|
| `panel_backtest.py` | 605-611 | `StartBacktest(self, event)` | Run backtest with selected strategy & parameters | Shows: "在线回测属于付费功能，请联系微信：Yida_Zhang2" |
| `panel_backtest.py` | 613-617 | `LoadData(self, event)` | Load market data for selected stock/period | Shows: "请联系微信：Yida_Zhang2 开通功能" |
| `panel_sim_trade.py` | 487 | `show_trade_boardview()` (else branch) | Show trading board for non-stock/BTC types | Shows: "交易平台尚未接入，请联系微信：Yida_Zhang2" |
| `panel_real_trade.py` | 488 | `show_trade_boardview()` (else branch) | Show trading board for non-stock/BTC types | Shows: "交易平台尚未接入，请联系微信：Yida_Zhang2" |

### 5.2 Engine-Level Stubs (Missing Implementations)

| File | Line | Component | Stub Description |
|------|------|-----------|------------------|
| `futures_engine.py` | 1-27 | `FuturesTradeEngine` | Entire class is a stub — only `__init__` and empty `start_trade()` with `pass` |
| `engine_apis/funds/` | — | Fund trading | **No engine file exists** — only `account.json.example` |
| `engine_apis/options/` | — | Options trading | **No engine file exists** — only `account.json.example` |
| `trade_sim.py` | ~70-125 | Fund/Options account loading | Accounts loaded but **no engine created** — code falls through |
| `trade_real.py` | ~70-125 | Fund/Options account loading | Same as above — accounts loaded but no engine created |
| `trade_engine.py` | 29 | `TradeEngine.load_strategy()` | Empty `pass` — no strategy loading implemented |
| `stock_engine.py` | EastmoneyTrader | `EastmoneyTrader.get_balance()` | Calls undefined `get_cash()` (should be `self.client.get_cash()`) |
| `stock_engine.py` | EastmoneyTrader | `EastmoneyTrader.start_trade()` | All order logic commented out |
| `btc_trade_engine.py` | OkxTradeEngine | `get_all_tickers()` | `pass` |
| `btc_trade_engine.py` | OkxTradeEngine | `get_positions()` | `pass` |
| `btc_trade_engine.py` | OkxTradeEngine | `get_order_book()` | `pass` |
| `btc_engine.py` | BtcTradeEngine | `get_balance()` | `pass` |
| `btc_engine.py` | BtcTradeEngine | `get_all_tickers()` | `pass` |
| `btc_engine.py` | BtcTradeEngine | `get_order_book()` | `pass` |
| `btc_engine.py` | BtcTradeEngine | `get_account()` | `pass` |
| `btc_engine.py` | BtcTradeEngine | `get_asset_balance()` | `pass` |
| `btc_engine.py` | BtcTradeEngine | `order_market_buy()` | `pass` |

### 5.3 Strategy Stubs (Macros "预留" Entries)

In `qbot/common/macros.py`, 17 of 25 strategy choices are marked with "(预留X)" — they appear in the UI dropdown but have **no backend implementation**:

| Marked | Strategy |
|--------|----------|
| 预留A | 单因子-随机相对强弱指数StochRSI |
| 预留B | 单因子-RSRS择时 |
| 预留C | 单因子-移动均线+KDJ |
| 预留D | 单因子-MACD和ADX指标 |
| 预留E | 单因子-布林线均值回归 |
| 预留F | 单因子-阿隆指标(趋势交易) |
| 预留G | 单因子-简单移动均线 |
| 预留H | 单因子-情绪指标ARBR |
| 预留I | 单因子-市场低估值策略 |
| 预留J | 机器学习-麻雀优化算法SSA |
| 预留K | 机器学习-LSTM时序预测 |
| 预留L | 机器学习-随机森林模型价格预测 |
| 预留M | 机器学习-线性回归价格预测 |
| 预留N | 强化学习-RL模型价格预测 |
| 预留O | 强化学习-Q-Leaning预测 |
| 预留P | 传统策略-海龟策略 |
| 预留Q | 传统策略-网格策略 |
| 预留R | 组合优化-配对交易 |
| 预留S | 组合优化-Kurtosis Portfolio组合策略 |
| 预留T | 多因子-小市值 |
| 预留U | 多因子-alphalens多因子交易 |

**Strategies with actual implementations** (standalone scripts in `qbot/strategies/`):
1. 单因子-相对强弱指数RSI (in `backtest_main.py`)
2. 单因子-布林线均值回归 (`boll_strategy_bt.py` — uses backtrader)
3. 机器学习-麻雀优化算法SSA (`ssa_strategy_bt.py` — but still marked "预留")
4. 机器学习-LSTM时序预测 (`lstm_strategy_bt.py` — but still marked "预留")
5. 强化学习-RL模型价格预测 (`rl_strategy_bt.py` — but still marked "预留")
6. 多因子-ROC(20)动量信号周频Top1 (no dedicated file)

**Critical gap:** The strategy scripts in `qbot/strategies/` are **standalone scripts** — they are NOT connected to the GUI's strategy selection dropdown. The dropdown lists strategy names but selecting one and clicking "开始回测" just shows the WeChat paywall.

### 5.4 Empty/Stub Files

| File | Status |
|------|--------|
| `qbot/strategies/boll_strategy.py` | Only contains file header comment — no code |
| `qbot/engine/tokens.py` | Referenced but **does not exist** |
| `qbot/gui/widgets/widgets.py` | Imported by `panel_results.py` but **does not exist** |

---

## 6. Data Flow Analysis

### 6.1 Data Entry Points

```
┌──────────────────────────────────────────────────────────┐
│                    DATA SOURCES                           │
├─────────────┬──────────────┬──────────────┬──────────────┤
│   tushare   │   akshare    │   baostock   │  新浪爬虫     │
│ (primary)   │ (backtest)   │  (planned)   │  (planned)  │
└──────┬──────┴──────┬───────┴──────┬───────┴──────┬───────┘
       │             │              │              │
       ▼             ▼              ▼              ▼
┌──────────────────────────────────────────────────────────┐
│              data/  (local storage)                       │
│  ├── stocks/    CSV files                                 │
│  ├── hdf5/      all.h5, cache.h5                         │
│  ├── futures/                                              │
│  ├── btc/                                                  │
│  ├── funds/                                                │
│  ├── options/                                              │
│  ├── multi-facts/  (multi-factor)                         │
│  └── qlib_data/    (Microsoft Qlib format)                 │
└──────────────────────┬───────────────────────────────────┘
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
    ┌────────────┐ ┌─────────┐ ┌──────────┐
    │  Backtest  │ │ Strategy│ │  Trade   │
    │   Engine   │ │ Scripts │ │  Engine  │
    │            │ │         │ │          │
    │ STUBBED    │ │ Stand-  │ │ Partial  │
    │ (paywall)  │ │ alone   │ │ (掘金+   │
    │            │ │ scripts │ │  ccxt)   │
    └────────────┘ └─────────┘ └──────────┘
           │           │           │
           ▼           ▼           ▼
    ┌──────────────────────────────────────┐
    │         results/                      │
    │  ├── bkt_result/  HTML/CSV results    │
    │  ├── hdf5/        HDF5 results        │
    │  └── indicators/  Indicator plots     │
    └──────────────────────────────────────┘
```

### 6.2 Backtest Data Flow (Designed, NOT Functional)

```
User selects params in PanelBacktest
    → backtest_opts dict assembled (start_time, end_time, code, strategy, benchmark)
    → backtest_config dict assembled (init_cash, slippage, commission, stake)
    → [STUB] StartBacktest() → shows WeChat paywall dialog
    
    Intended flow (not implemented):
    → Load data from data/stocks/ or API
    → Instantiate BacktestStrategyTemplate subclass
    → Run backtest via backtrader or custom engine
    → Generate HTML/plot results
    → Display in WebPanel via show_file()
```

### 6.3 Live Trading Data Flow (Partially Functional)

```
User selects params in SimTradePanel/RealTradePanel
    → trader_opts dict: {class, platform, trade_type, trade_code, strategy}
    → TradeEngine instantiated
        → Routes to SimTradeEngine or RealTradeEngine based on class
            → Routes to platform-specific engine based on trade_type + platform
                → StockTradeEngine → GmSimTrader (掘金) / EastmoneyTrader
                → FuturesTradeEngine → [STUB - only pass]
                → BtcTradeEngine → BinanceTradeEngine / OkxTradeEngine / CcxtTradeEngine
                → Fund/Options → [NO ENGINE]
    → login() → platform-specific auth
    → get_positions() → fetch current holdings
    → start_trade() → [STUB in most engines - strategy not loaded]
```

### 6.4 Data Storage

- **Primary:** Local CSV files in `data/stocks/`
- **Secondary:** HDF5 files (`data/hdf5/all.h5`, `cache.h5`)
- **Config storage:** `qbot/common/configs/*.json` (sys_para, firm_para, back_para, trade_plat_para)
- **Account storage:** `qbot/engine/trade/engine_apis/*/account.json` (credentials — example files only)
- **Results:** HTML files displayed in WebView, CSV files in `results/`
- **Config also supports:** Sqlite (radio button in ParamsConfigDialog, but unimplemented)

---

## 7. Backend / Engine Components

### 7.1 Trade Engine Hierarchy

```
TradeEngine (Facade)
├── SimTradeEngine
│   ├── StockTradeEngine
│   │   ├── GmSimTrader       ✓ Functional (掘金量化平台, gmtrade API)
│   │   └── EastmoneyTrader   ⚠ Partial (login=pass, get_balance uses undefined get_cash)
│   ├── FuturesTradeEngine    ✗ Stub (start_trade = pass)
│   ├── BtcTradeEngine
│   │   ├── BinanceTradeEngine ✓ Functional (python-binance)
│   │   ├── OkxTradeEngine     ⚠ Partial (many methods = pass, API auth broken)
│   │   └── CcxtTradeEngine    ✓ Functional (ccxt multi-exchange)
│   ├── FundTradeEngine       ✗ Does not exist
│   └── OptionTradeEngine     ✗ Does not exist
│
└── RealTradeEngine
    └── (same hierarchy as SimTradeEngine)
```

### 7.2 easytrader Integration

A full copy of the `easytrader` library is bundled at `qbot/engine/trade/easytrader/`. It provides:
- Broker adapters for: 同花顺, 华泰证券(ht_client), 通达信, 银河证券, 雪球, 国金(gj), 国信(gf), 恒投证券(htzq), 万科(wk)
- `ClientTrader` base class with GUI automation (Windows-only)
- `JoinQuantFollower` and `RiceQuantFollower` for following platform strategies
- Uses Selenium/ChromeDriver for web-based broker interaction

### 7.3 CTP Futures Trader (`qbot/engine/trade/trader/`)

A Django-based CTP (China futures) trading application:
- `panel/` — Django web panel for monitoring
- `trader/` — Core CTP trading logic with strategy support
- `utils/` — API structures, data fetching, logging
- Uses `brother2` strategy

### 7.4 Bitcoin Arbitrage (`qbot/engine/trade/trading/bitcoin-arbitrage/`)

A complete Bitcoin arbitrage engine:
- Observer pattern with email, XMPP, logging observers
- Public market support: Binance, Bitfinex, Bitflyer, Bitstamp, BTCC, CEX, GDAX, Gemini, Kraken, OKCoin
- Private market support: Bitstamp, Paymium
- Arbitrage detection and execution logic

---

## 8. Strategy Framework

### 8.1 Strategy Execution Models

The codebase has **two disconnected** strategy frameworks:

**Framework 1: Backtrader-based (Standalone Scripts)**
- Located in `qbot/strategies/`
- Each file is a self-contained script with `if __name__ == "__main__"` block
- Uses `backtrader` library for backtesting
- Data fetched via `akshare` or `tushare`
- NOT connected to the GUI

**Framework 2: Template-based (GUI-intended)**
- `qbot/engine/backtest/backtest_base.py` defines `BacktestStrategyTemplate`
- Has `get_singal()`, `get_scores()`, `process()`, `output_earning_rate()`, `show_plt()` methods
- Referenced by `backtest_main.py` which imports `from RSI import RSIStrategy`
- NOT connected to the GUI either (GUI shows paywall)

### 8.2 Strategy Coverage

| Category | Count | Implemented | Stub |
|----------|-------|-------------|------|
| 单因子 (Single Factor) | 9 | 1 (RSI) | 8 |
| 机器学习 (ML) | 5 | 0 (scripts exist but not connected) | 5 |
| 强化学习 (RL) | 2 | 0 | 2 |
| 传统策略 (Traditional) | 2 | 0 | 2 |
| 组合优化 (Portfolio) | 2 | 0 | 2 |
| 多因子 (Multi-factor) | 2 | 0 | 2 |
| **Total** | **25** | **1** | **24** |

### 8.3 TreeList Strategy Navigation

`CollegeTreeListCtrl` provides a hardcoded tree of strategy categories:
- **经典策略:** N日突破, ATR止盈止损
- **自定义策略:** yx-zl-1/2/3 (未定义)
- **衍生指标:** 均线交叉, 跳空缺口, 黄金分割
- **K线形态:** 乌云盖顶, 三只乌鸦, 十字星, 锤头, 射击之星

Clicking these items in the tree triggers `_ev_click_on_treelist` which shows a MessageDialog but does NOT load any strategy.

---

## 9. Extensibility Assessment

### 9.1 Well-Structured Modules (Easy to Extend)

| Module | Why |
|--------|-----|
| **WebPanel** | Clean WebView wrapper, easy to add new web views |
| **GridTable** | Good wx.grid wrapper with DataFrame support |
| **TradeEngine facade** | Clean routing pattern between sim/real |
| **CcxtTradeEngine** | Multi-exchange support via ccxt, adding new exchanges is trivial |
| **BtcTradeEngine hierarchy** | Good platform abstraction, easy to add new crypto exchanges |
| **SysLogIf / PrintLog** | Clean log interface |
| **JSON config system** | Simple file-based config, easy to extend |
| **Strategy tree** | Clean UI for strategy navigation, easy to add entries |

### 9.2 Tightly Coupled / Needs Refactoring

| Module | Issues |
|--------|--------|
| **PanelBacktest** | 600+ lines in a single class, no separation of concerns, UI + logic mixed |
| **SimTradePanel / RealTradePanel** | Near-identical code (~500 lines each), should share a base class |
| **TradeEngine.load_strategy()** | Empty — strategy loading not connected to trading |
| **Config duplication** | `qbot/common/config.py` and `qbot/engine/config.py` are identical |
| **panel_results.py** | Imports non-existent `widgets.py` module — completely broken |
| **OkxTradeEngine** | Mixes Binance and OKX code, has undefined variables (`base_url`), `get_account()` calls `self.client` which doesn't exist |
| **BacktestBase** | Disconnected from GUI; GUI shows paywall instead of using the framework |
| **Strategy selection** | Dropdown shows 25 strategies but no routing to actual implementations |
| **Account JSON handling** | Real credentials would be in version control (account.json files in source tree) |

### 9.3 Architecture Gaps

1. **No strategy → GUI bridge:** Strategy scripts exist but can't be invoked from the GUI
2. **No real backtesting pipeline:** The GUI backtest button is stubbed; only standalone scripts work
3. **No data management layer:** No abstraction for fetching/caching/updating market data
4. **No event system:** GUI and engine communicate through direct method calls, no pub/sub
5. **No plugin loading:** Strategy "plugins" are hardcoded in macros.py
6. **Missing modules:** `tokens.py`, `widgets.py` — critical for functionality

---

## 10. Third-Party Dependencies

From `requirements.txt`:

| Dependency | Purpose | Notes |
|------------|---------|-------|
| **wxPython** | GUI framework | Core UI framework |
| **pandas** | Data manipulation | Used throughout |
| **matplotlib** | Plotting | 3.2.2 pinned |
| **backtrader** | Backtesting engine | Strategy framework |
| **pyfolio** | Portfolio analytics | Installed from git |
| **backtrader_plotting** | Backtrader visualization | |
| **scipy** | Scientific computing | |
| **statsmodels** | Statistical models | |
| **quantstats** | Portfolio statistics | Bundled in plugins/ |
| **requests** | HTTP client | |
| **loguru** | Logging | |
| **binance-connector** | Binance API | |
| **ta-lib** | Technical analysis | Platform-specific install |
| **numpy** | Numerical computing | |
| **pillow** | Image processing | |
| **pykalman** | Kalman filter | |
| **scikit-learn** | ML library | SVM, RF, etc. |
| **empyrical** | Financial metrics | |
| **jupyter** | Notebook server | For embedded notebooks |
| **tensorboard** | TF visualization | |
| **tensortrade** | RL trading framework | |
| **yfinance** | Yahoo Finance data | |
| **efinance** | East Money data | |
| **akshare** | Chinese market data | Used in strategy scripts |
| **pandas_datareader** | Data source abstraction | |
| **tushare** | Chinese stock data | Used in qbot_main.py, qbot.py |
| **easytrader** | Chinese broker trading | Bundled in engine/ |
| **gmtrade** | 掘金 quantitative platform | |
| **ccxt** | Crypto exchange library | |
| **tensorflow/keras** | Deep learning | LSTM, models |

---

## 11. Key Findings & Recommendations

### 11.1 Summary of What Works

1. **GUI shell** — The wxPython UI is well-structured with proper panel hierarchy, menus, and parameter capture
2. **Crypto trading (Binance)** — `BinanceTradeEngine` has real API integration
3. **Crypto trading (multi-exchange)** — `CcxtTradeEngine` supports 10+ exchanges via ccxt
4. **Stock sim trading (掘金)** — `GmSimTrader` connects to MyQuant simulation API
5. **Knowledge hub** — Research report viewer and Jupyter integration work
6. **Strategy scripts** — Several complete backtrader-based strategies exist (Bollinger, SMA, RL, LSTM)
7. **Arbitrage engine** — Complete BTC arbitrage system with multi-exchange support

### 11.2 Critical Issues to Address

1. **Missing `tokens.py`** — All API token imports will fail. Need to create this file with actual credentials or a credential management system.

2. **Missing `widgets.py`** — `ResultsPanel` is completely broken. Need to create `qbot/gui/widgets/widgets.py` with `MatplotlibPanel` and `PandasGrid` classes.

3. **Config duplication** — `qbot/common/config.py` and `qbot/engine/config.py` are identical. Consolidate to one.

4. **No backtesting pipeline** — The entire backtest flow from GUI → strategy execution → results display is stubbed. This is the core feature that needs building.

5. **Strategy-GUI disconnect** — 18 strategy implementations exist in `qbot/strategies/` but are standalone scripts. Need a strategy registry and execution bridge.

6. **Sim/Real panel duplication** — `panel_sim_trade.py` and `panel_real_trade.py` share 90%+ code. Extract common base class.

7. **Fund/Options trading** — Account structure exists but no engine implementations.

8. **Security** — Account credentials stored as JSON files in source tree. Need proper credential management.

### 11.3 Recommended Refactoring Priorities

1. **P0 — Create missing modules:** `tokens.py`, `widgets.py`
2. **P0 — Fix broken imports:** panel_results.py, tokens references
3. **P1 — Build backtesting bridge:** Connect GUI strategy selection to backtrader strategy execution
4. **P1 — Strategy registry:** Create a strategy factory/registry that maps macro names to strategy classes
5. **P2 — Extract panel base class:** Merge SimTradePanel/RealTradePanel common code
6. **P2 — Data layer abstraction:** Unified data fetching with caching
7. **P3 — Credential management:** Move to environment variables or encrypted storage
8. **P3 — Event system:** Decouple GUI from engine with pub/sub pattern

---

*End of Architecture Analysis*
