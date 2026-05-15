# Qbot 代码审计报告

**日期:** 2026-05-14
**审计范围:** 全代码库 — README.md, docs/, qbot/gui/, qbot/strategies/, qbot/engine/, qbot/plugins/, qbot/data/, qbot/common/
**Linear Issue:** RUO-264

---

## 执行摘要

Qbot 在 README 和文档中宣传了 **186 个功能点**，涵盖数据获取、策略开发、回测、模拟交易、实盘交易、AI 选股、通知系统等 20 个类别。

经过全面扫描，审计发现：

| 分类 | 数量 | 占比 |
|------|------|------|
| 完整实现 | ~28 | 15% |
| 部分实现 | ~22 | 12% |
| 付费墙/联系墙 Stub | ~12 | 6% |
| 纯壳子/预留/未实现 | ~124 | 67% |

**关键发现：**
- **67% 的宣传功能是纯壳子**（文件为空、只有 TODO/预留注释、或策略被标记为"预留"）
- **6 个核心功能存在微信联系墙**（需要联系 `Yida_Zhang2` 才能使用）
- **3 个策略文件会在运行时崩溃**（RL、RSRS、多因子选股）
- **2 个硬编码 API Token 暴露在源码中**（Tushare、GMTrade）
- **GUI 中 12 个高严重性 bug** 导致核心功能不可用

---

## 审计方法论

1. 读取 README.md 和 docs/ 下所有文件，提取 186 个宣传功能点
2. 扫描 qbot/gui/ 下 20 个 Python 文件（GUI 面板、对话框、主窗口）
3. 扫描 qbot/ 下 ~180 个 Python 文件（策略、引擎、插件、数据层）
4. 搜索模式：`wx.MessageBox`, `微信`, `联系`, `paywall`, `TODO`, `pass`, `NotImplementedError`, 空函数体, 注释掉的代码, 未绑定的事件处理

---

## 一、GUI 层审计结果

### 高严重性问题 (12个)

| ID | 文件 | 行号 | 问题 | 影响功能 |
|----|------|------|------|----------|
| GH1 | mainframe.py | 107-113 | `start_monitoring` 逻辑反转 + `grep_pid` 未导入 | 后台监控完全不可用 |
| GH2 | mainframe.py | 139-141 | TODO: 多线程加载标签页 | 启动性能差 |
| GH3 | mainframe.py | 143-148 | 注释掉的面板: 在线交易、用户框架、资产轮动 | 3 个标签页被禁用 |
| GH4 | mainframe.py | 131-133 | 硬编码外部 IP 地址 | AI 选股/选基 依赖外部服务器 |
| GH5 | def_dialog.py | 628, 695 | 微信联系墙: `联系Yida_Zhang2 获取自动化实盘交易接口` | 实盘交易配置被封锁 |
| GH6 | panel_sim_trade.py | 487 | 微信联系墙: `请联系微信：Yida_Zhang2` | 基金/期货交易不可用 |
| GH7 | panel_backtest.py | 563-569 | `self.code_table` 未定义 | 股票代码输入回车崩溃 |
| GH8 | panel_results.py | 21 | 导入不存在的 `widgets.widgets` 模块 | 结果面板完全不可用 |
| GH9 | mainframe.py | 71-76 | `on_menu` 创建面板但从不添加到标签页 | 蛋卷估值、集思录菜单无效 |
| GH10 | def_dialog.py | 45-61 | `WebDialog` 定义但从未使用 | 死代码 |
| GH11 | def_dialog.py | 63-83 | `InputsDialog` 定义但从未使用 | 死代码 |
| GH12 | panel_results.py | 23-166 | `ResultsPanel` 死代码，从未实例化 | 完全不可用 |

### 微信联系墙/付费墙 (6处)

| 文件 | 行号 | 弹窗内容 | 被封锁功能 |
|------|------|----------|-----------|
| def_dialog.py | 628 | `微信联系Yida_Zhang2 获取自动化实盘交易接口后，填写参数` | 股票实盘交易 API 配置 |
| def_dialog.py | 695 | `微信联系Yida_Zhang2 或者自行获取{trade_plat}账户uid后，填写参数` | 交易平台账户配置 |
| panel_sim_trade.py | 487 | `交易平台尚未接入，请联系微信：Yida_Zhang2` | 基金/期货模拟交易 |
| panel_real_trade.py | 488 | `交易平台尚未接入，请联系微信：Yida_Zhang2` | 基金/期货实盘交易 |
| mainframe.py | 95 | 状态栏: `请关注公众号: 迈微AI研习社` | UI 广告植入 |
| mainframe.py | 83-87 | 关于对话框仅显示公众号名称 | 关于页面无版本信息 |

### 中严重性问题 (17个)

| ID | 文件 | 问题 |
|----|------|------|
| GM1 | panel_backtest.py:502 | 交易日志按钮无事件绑定 |
| GM2 | panel_backtest.py:626 | `_ev_trade_log` 空函数 (bare pass) |
| GM3 | panel_backtest.py:157-163 | 注释掉的"条件选股"和"形态选股"标签 |
| GM4 | panel_backtest.py:293-311 | 多子图显示和投资组合分析下拉框未绑定 |
| GM5 | panel_backtest.py:405-461 | 回测参数输入框变更事件未绑定 |
| GM6 | panel_backtest.py:49-51 | 未使用的 stub 函数 `OnBkt` |
| GM7 | panel_sim_trade.py:421 | 注释掉的微信联系墙 (原先是付费墙) |
| GM8 | panel_sim_trade.py:437-443 | 硬编码交易参数覆盖用户选择 |
| GM9 | panel_sim_trade.py:151 | 股票池双击处理函数为空 |
| GM10 | panel_sim_trade.py:499-527 | 策略导航树逻辑错误，始终显示"当前点击:0!" |
| GM11 | panel_sim_trade.py:489-497 | 交易日志对话框 OK/Cancel 处理为空 |
| GM12 | def_dialog.py:737 | `_ev_switch_menu` 空函数 |
| GM13 | def_treelist.py:29-31 | 自定义策略标记为"未定义" |
| GM15 | panel_sim_trade.py:302 | `multi_fact_layout()` 方法不存在，选择多因子策略崩溃 |
| GM16 | panel_trade.py:23 | "我的自选"标签被注释掉 |
| GM17 | mainframe.py:39-68 | 菜单栏仅 3 个菜单 5 个项目，无工具栏 |
| GM18 | widget_matplotlib.py:13 | "投资策略回测分析"按钮无事件绑定 |

---

## 二、后端/策略层审计结果

### 高严重性问题 (14个)

| ID | 文件 | 行号 | 问题 | 影响功能 |
|----|------|------|------|----------|
| BH1 | arbr_strategy.py | 33 | 硬编码 Tushare API Token: `6f747880359ef14f...` | 安全漏洞 |
| BH2 | gmtrade_example.py | 22,28 | 硬编码 GMTrade Token 和账户 ID | 安全漏洞 |
| BH3 | 多个策略文件 | — | 4 个策略文件为空（仅有 license header） | bigger_than_ema, boll_strategy 等不可用 |
| BH4 | rl_strategy_bt.py | 51 | `self.model` 未定义，运行时崩溃 | RL 策略完全不可用 |
| BH5 | rl_strategy_bt.py | 44-45 | `__init__` 在数据就绪前运行训练 | RL 策略设计错误 |
| BH6 | btc_engine.py | 36-59 | BTC 交易引擎 7 个方法全部是 `pass` | BTC 交易完全不可用 |
| BH7 | futures_engine.py | 13 | 期货交易引擎 `start_trade()` 只有 `pass` | 期货交易完全不可用 |
| BH8 | btc_trade_engine.py | 131-211 | OkxTradeEngine 引用未定义变量 | OKEX 交易崩溃 |
| BH9 | btc_trade_engine.py | 237-309 | HuobiTradeEngine 复制粘贴使用 Binance Client | 火币交易实际连接币安 |
| BH10 | btc_trade_engine.py | 482 | CcxtTradeEngine 缺少 `self.` 前缀 | 止损止盈逻辑崩溃 |
| BH11 | trade_engine.py | 37-56 | `load_strategy()` 全部是 stub | 策略加载未实现 |
| BH12 | 4个文件 | — | `load_strategy()` 在所有交易引擎中均为 `pass` | 交易引擎无法执行任何策略 |
| BH13 | stock_engine.py | 160-168 | EastmoneyTrader 调用未定义的函数 | 东方财富交易崩溃 |
| BH14 | private_markets/market.py | — | 比特币套利 5 个方法全部 `raise NotImplementedError` | 比特币套利完全不可用 |

### 策略实现状态

| 策略 | 文件 | 状态 | 能否运行 |
|------|------|------|----------|
| RSI | rsi_strategy_bt.py | 已实现（无独立运行入口） | 需要外部数据接入 |
| SMA Cross | sma_cross_strategy_bt.py | 已实现 | 可以运行（模块级副作用） |
| EMA Bigger | bigger_than_ema_bt.py | 已实现 | 可以运行（模块级副作用） |
| Bollinger | boll_strategy_bt.py | 已实现 | 可以运行 |
| Multi (RSI+SMA) | multi_strategy_bt.py | 已实现 | 可以运行（模块级副作用） |
| LSTM | lstm_strategy_bt.py | 部分实现（每次重新训练） | 极慢，可用但不实用 |
| **RL** | rl_strategy_bt.py | **损坏**（无模型） | **运行时崩溃** |
| SSA | ssa_strategy_bt.py | 已实现 | 可以运行 |
| ARBR | arbr_strategy.py | 已实现（硬编码 token） | 可以运行 |
| ADX+MACD | adx_strategy.py | 已实现 | 可以运行 |
| K-Lines | k_lines_bt.py | 已实现 | 可以运行 |
| **RSRS** | rsrs.py | **有 Bug**（未定义变量） | **运行时崩溃** |
| Undervalued | undervalued_stock_picking_strategy.py | 仅 JoinQuant 平台 | 不能独立运行 |
| MACD BT | macd_bt.py | 已实现 | 可以运行 |
| Bitcoin BT | bitcoin_bt_example.py | 需要 Amberdata API Key | 需要配置 |

---

## 三、功能完整性分类

### 完整实现 (~28个, 15%)

| 功能 | 证据 | 备注 |
|------|------|------|
| GUI 桌面客户端 | mainframe.py 完整实现 | 有 bug 但基本功能可用 |
| 可视化回测系统 | panel_backtest.py 完整实现 | 核心功能可用 |
| Backtrader 集成 | 多个 _bt.py 策略使用 backtrader | 运行正常 |
| SMA Cross 策略 | sma_cross_strategy_bt.py | 完整 |
| Bollinger 策略 | boll_strategy_bt.py | 完整 |
| EMA Bigger 策略 | bigger_than_ema_bt.py | 完整 |
| Multi-Strategy | multi_strategy_bt.py | 完整 |
| SSA 麻雀搜索策略 | ssa_strategy_bt.py | 完整 |
| ARBR 策略 | arbr_strategy.py | 完整（有硬编码 token） |
| ADX+MACD 策略 | adx_strategy.py | 完整 |
| K-Lines 策略 | k_lines_bt.py | 完整 |
| MACD 回测示例 | macd_bt.py | 完整 |
| RSI 策略 | rsi_strategy_bt.py | 完整（无独立入口） |
| Tushare 数据接入 | 多个文件使用 tushare | 正常 |
| AKShare 数据接入 | boll_strategy_bt.py | 正常 |
| 数据本地缓存 | CSV 存储逻辑存在 | 正常 |
| 股票指标计算 | docs/股票指标.md + 代码 | 部分实现 |
| 策略导航树 | def_treelist.py | UI 存在但有逻辑错误 |
| 参数配置对话框 | def_dialog.py | 大部分可用 |
| 策略回测分析图 | widget_matplotlib.py | 可用 |
| 基准曲线 | panel_backtest.py 中实现 | 可用 |
| 交易指标面板 | GUI 中可显示 | 基本可用 |
| Python 策略框架 | backtrader-based | 可扩展 |
| 佣金/滑点配置 | panel_backtest.py 参数区 | 可用 |
| A股数据支持 | tushare/baostock | 正常 |
| 港股数据支持 | 最近 commit 添加 | 正常 |
| Quantstats 报告 | backend/quantstats/ | 存在 |
| Docker 支持 | docs/Install_guide.md 描述 | 文档存在 |

### 付费墙/联系墙 Stub (~12个, 6%)

| 功能 | 被封锁方式 | 文件:行号 |
|------|-----------|----------|
| 自动化实盘交易接口配置 | 微信联系 Yida_Zhang2 | def_dialog.py:628 |
| 交易平台账户参数填写 | 微信联系 Yida_Zhang2 | def_dialog.py:695 |
| 基金模拟交易 | "交易平台尚未接入，请联系微信" | panel_sim_trade.py:487 |
| 基金实盘交易 | "交易平台尚未接入，请联系微信" | panel_real_trade.py:488 |
| 期货模拟交易 | "交易平台尚未接入，请联系微信" | panel_sim_trade.py:487 |
| 期货实盘交易 | "交易平台尚未接入，请联系微信" | panel_real_trade.py:488 |
| Qbot Pro 完整闭环 | README 中标记为付费版 | README.md:651 |
| VIP 版本一对一服务 | README 中标记为 VIP | README.md:652 |
| 策略服务市场 | README 宣传 | README.md:636-639 |
| 知识星球社区 | README 宣传为付费社区 | README.md:753-754 |
| 高级指标 (主力意图等) | README 中标记为付费 | README.md:490-502 |
| AI 股票推荐邮件订阅 | README 宣传 | README.md:805 |

### 部分实现 (~22个, 12%)

| 功能 | 状态 | 问题描述 |
|------|------|----------|
| AI 选股/选基 | 依赖硬编码外部 IP | mainframe.py:131 — 服务器可能不可用 |
| ChatGPT 策略编写 | 依赖第三方 URL | mainframe.py:129 — URL 可能失效 |
| LSTM 预测策略 | 每次回测重新训练 50 epoch | lstm_strategy_bt.py — 极慢 |
| Jupyter Notebook 集成 | 按钮不启动服务器 | panel_zhiku.py:131 |
| RSRS 择时策略 | 有未定义变量 Bug | rsrs.py:148 |
| 比特币回测 | 需要手动配置 API Key | bitcoin_bt_example.py |
| 币安实盘交易 | 需要手动配置 API Key | live_trade_binance.py |
| 交易日志查看 | 对话框存在但 OK/Cancel 为空 | panel_sim_trade.py:489 |
| 多因子策略选择 | `multi_fact_layout()` 未定义 | panel_sim_trade.py:302 |
| 条件选股/形态选股 | 标签页被注释掉 | panel_backtest.py:157 |
| 投资组合分析 | 下拉框未绑定事件 | panel_backtest.py:293 |
| 多子图显示 | 下拉框未绑定事件 | panel_backtest.py:311 |
| 后台监控 | 逻辑反转 + 缺少导入 | mainframe.py:107 |
| 在线交易标签 | 被注释掉 | mainframe.py:143 |
| Dagster 批处理 | 硬编码测试数据 | dagster_taskgraph.py:15 |
| 自动监控插件 | 模块级无限循环 | auto_monitor.py:123 |
| 技术指标 (30+) | 代码中只实现部分 | 文档声称 30+，代码中约 10+ |
| Alpha-101/191 因子 | README 宣传，代码中未找到实现 | 仅文档提及 |
| DEAP 自动因子生成 | README 宣传，代码中未找到实现 | 仅文档提及 |
| 因子表达式引擎 | README 宣传，代码中未找到实现 | 仅文档提及 |
| 4433 基金法则 | 文档描述，无对应代码实现 | docs/ 中有描述 |
| 网格交易策略 | 文档描述，代码中为 stub | docs/ 中有描述 |

### 纯壳子/预留/未实现 (~124个, 67%)

#### 交易 API 接入 (25个)

README 宣传 25 个交易 API 接入（期货 CTP/CTPMini/Femas、期权 CTPOpt/MA Opt/QWIN、股票 XTP/同花顺/东方财富/华泰/国泰君安 等、加密货币 OKEX/币安/火币），实际代码中：

- **期货引擎**: 只有 `pass` (futures_engine.py:13)
- **BTC 引擎**: 7 个方法全部 `pass` (btc_engine.py:36-59)
- **OkxTradeEngine**: 引用未定义变量，运行崩溃
- **HuobiTradeEngine**: 复制粘贴错误，实际连接币安
- **EastmoneyTrader**: 调用未定义函数
- **比特币套利引擎**: 5 个方法 `raise NotImplementedError`

#### AI/ML 策略 (20+个)

README 宣传 300+ AI 模型、40+ 论文，包括 LightGBM, SVM, Q-Learning, Random Forest, XGBoost, CatBoost, DoubleEnsemble, TabNet, Linear Regression, MLP, GRU, ALSTM, ADARNN, ADD, KRNN, Sandwich, TFT, GATs, SFM, Transformer, TCTS, TRA, TCN, IGMTF, HIST, Localformer, ChatGPT, FinGPT 等。

实际代码中：
- **RL 策略**: 运行崩溃 (rl_strategy_bt.py)
- **LSTM**: 可用但不实用（每次重新训练）
- **其他 20+ ML 模型**: 无任何代码实现，仅在 README 中列出

#### 策略预留 (17个)

qbot/qbot.py 配置文件中 17/28 个策略标记为"预留"：
StochRSI, RSRS, MACD+ADX, Bollinger, Aroon, SMA, ARBR, Undervalued, SSA, SVM, LSTM, LGBM, Random Forest, Linear Regression, RL, Q-Learning, Turtle, Grid, Pair Trading, Kurtosis Portfolio, Multi-factor

#### GUI 禁用功能 (8+个)

- Qbot 量化投研面板（UserFrame 被注释掉）
- 资产轮动策略分析面板（ActionsPanel 被注释掉）
- 我的自选/关注标签（FocusSymsPanel 不存在）
- 蛋卷估值菜单（创建了面板但未显示）
- 集思录菜单（创建了面板但未显示）
- 交易策略在线交易标签（被注释掉）

#### 通知系统 (6个)

README 宣传 6 种通知方式：邮件、飞书、系统弹窗、微信、钉钉、企业微信。代码中无任何通知系统实现。

#### 其他未实现功能

- 实时数据（秒级）：README TODO 项，无代码
- WeChat 小程序：README 宣传，无代码
- Docker 部署：文档描述为"开发中"
- 实盘自动化交易：README 宣传，被微信联系墙封锁
- 模拟交易延迟/滑坡模拟：README 宣传，代码为 stub
- 策略鲁棒性测试：仅文档描述
- 基金对冲策略：仅 README 列出
- 智赢多因子策略：仅 README 列出
- 惠赢智能算法：仅 README 列出

---

## 四、安全漏洞

| 严重性 | 文件 | 行号 | 问题 |
|--------|------|------|------|
| **严重** | arbr_strategy.py | 33 | Tushare Pro API Token 硬编码: `6f747880359ef14f...` |
| **严重** | gmtrade_example.py | 22,28 | GMTrade Token + 账户 ID 硬编码 |
| **中等** | dagster_taskgraph.py | 15 | 硬编码测试数据覆盖真实数据查询 |
| **中等** | auto_monitor.py | 74 | Token 占位符 `"your token"` |
| **低** | easytrader_example.py | 51 | 用户名密码占位符 |

---

## 五、代码质量问题汇总

### 会崩溃的 Bug (运行时 NameError/AttributeError)

| 文件 | 行号 | 问题 |
|------|------|------|
| rl_strategy_bt.py | 51 | `self.model` 未定义 |
| rl_strategy_bt.py | 60 | `self.log()` 未定义 |
| rsrs.py | 148 | `stock_code` 未定义 |
| stock_engine.py | 160-168 | `get_cash()` 和 `get_positions()` 未定义 |
| btc_trade_engine.py | 482 | `exchange` 缺少 `self.` 前缀 |
| btc_trade_engine.py | 131-211 | `self.api_secret` 等未正确赋值为实例属性 |
| futures_engine.py | 24 | `self` 在模块作用域中未定义 |
| panel_backtest.py | 563 | `self.code_table` 未定义 |
| panel_sim_trade.py | 302 | `multi_fact_layout()` 方法不存在 |
| trade_sim.py | 49 | `accounts` 变量应为 `sim_accounts` |
| util.py | 58 | `np` 未导入 |

### 模块级副作用（导入即执行）

| 文件 | 行号 | 问题 |
|------|------|------|
| multi_strategy_bt.py | 107 | 模块级调用 `get_data("600018")` |
| sma_cross_strategy_bt.py | 82-83 | 模块级调用 `get_data(...)` |
| bigger_than_ema_bt.py | 130 | 模块级调用 `get_data("600018")` |
| lstm_strategy_bt.py | 104 | 模块级调用 `get_data("600018")` |
| auto_monitor.py | 123 | 模块级 `while True` 无限循环 |
| qbot.py | 39 | 模块级调用 `get_data("600018")` |

---

## 六、功能矩阵：宣传 vs 实现

| 类别 | 宣传数量 | 已实现 | 部分实现 | Stub/未实现 |
|------|----------|--------|----------|-------------|
| 平台架构 | 16 | 8 | 3 | 5 |
| 数据层 | 7 | 4 | 1 | 2 |
| 交易指标 | 7 | 2 | 2 | 3 |
| 经典策略 | 16 | 8 | 2 | 6 |
| 组合因子策略 | 8 | 3 | 1 | 4 |
| AI/ML 策略 | 32 | 2 | 1 | 29 |
| 智能交易策略 | 6 | 0 | 1 | 5 |
| 基金策略 | 7 | 1 | 1 | 5 |
| 回测系统 | 9 | 6 | 1 | 2 |
| 模拟/实盘交易 | 8 | 0 | 2 | 6 |
| 交易 API (期货/期权/股票/加密) | 25 | 0 | 3 | 22 |
| 通知系统 | 7 | 0 | 0 | 7 |
| 分析评估 | 6 | 2 | 1 | 3 |
| 风控/组合管理 | 5 | 1 | 1 | 3 |
| AI 选股/选基 | 3 | 0 | 2 | 1 |
| CI/CD | 4 | 4 | 0 | 0 |
| Qbot Pro (付费) | 6 | 0 | 0 | 6 |
| 开发者/社区 | 6 | 2 | 0 | 4 |
| 教育内容 | 4 | 4 | 0 | 0 |
| 券商客户端 | 4 | 0 | 0 | 4 |
| **合计** | **186** | **~47** | **~22** | **~117** |

---

## 七、优先修复建议

### P0 — 立即修复（安全 + 崩溃）

1. **移除硬编码 API Token**（arbr_strategy.py:33, gmtrade_example.py:22,28）→ 使用环境变量
2. **修复 RL 策略崩溃**（rl_strategy_bt.py）→ 要么实现模型加载，要么标记为不可用
3. **修复 RSRS 策略崩溃**（rsrs.py:148）→ 修复未定义变量
4. **修复多因子策略选择崩溃**（panel_sim_trade.py:302）→ 定义缺失的方法
5. **修复 HuobiTradeEngine 复制粘贴错误**（btc_trade_engine.py:237-309）

### P1 — 高优先级（核心功能）

6. **移除微信联系墙**（6 处）→ 替换为 API 配置文档
7. **修复 `load_strategy()` stub**（4 个文件）→ 实现策略加载机制
8. **修复期货/BTC 交易引擎 stub**（futures_engine.py, btc_engine.py）
9. **修复模块级副作用**（6 个文件）→ 移入 `__main__` 块
10. **修复 GUI 菜单项无效**（mainframe.py:71-76）→ 将面板添加到标签页

### P2 — 中优先级（用户体验）

11. **清理策略配置**（qbot/qbot.py）→ 只列出已实现的策略
12. **修复交易日志按钮**（panel_backtest.py:502）→ 绑定事件
13. **修复 Jupyter Notebook 启动**（panel_zhiku.py:131）→ 调用 `start_online_notebook()`
14. **替换硬编码外部 URL**（mainframe.py:131）→ 可配置化
15. **修复 `InputDialogTwoParameters.OnOk` bug**（def_dialog.py:140）→ 读取 text_ctrl2

### P3 — 低优先级（代码质量）

16. **替换 `iteritems()`**（def_grid.py:71）→ 使用 `items()`
17. **修复 bare `except:` 子句**（5 处）→ 添加具体异常类型和日志
18. **移除死代码**（WebDialog, InputsDialog, ResultsPanel）
19. **修复 setup.py 入口点**（sample → qbot）
20. **清理未使用的导入**

---

## 八、结论

Qbot 的 **核心回测功能（基于 Backtrader）是可用的**，包括约 10 个完整实现的经典策略和基本的 GUI 回测界面。但 README 宣传的 186 个功能中，约 67% 是纯壳子或未实现，6% 被付费墙/联系墙封锁。代码中存在 11 处运行时崩溃 bug 和 2 处硬编码 API Token 安全漏洞。

建议优先修复安全问题，然后逐步清理 stub 和联系墙，同时更新 README 使其准确反映实际实现状态。
