# Qbot Advertised Features Audit

> Generated from exhaustive review of README.md, all files under docs/, setup.py, requirements.txt,
> GitHub Actions workflows, GUI mainframe source, and source code comments.
> Date: 2026-05-14 (updated with deeper audit)

---

## Category: Platform Overview & Architecture

1. **AI-Oriented Quantitative Investment Platform** — Qbot is described as an AI-oriented automated quantitative investment platform supporting supervised learning, market dynamics modeling, and RL. (Source: README.md:52)
2. **Full Closed-Loop Quantitative Trading** — Provides the full workflow from data acquisition, strategy development, strategy backtesting, simulated trading to live trading. (Source: README.md:82, docs/README.md:80)
3. **Modular Layered Architecture** — Seven-layer design: Data Layer, Strategy Layer, Engine Layer, Interface Layer, Notification Layer, Analysis Layer, Extension Layer. (Source: docs/DEVELOPMENT.md:10-23)
4. **Event-Driven Trading Flow** — Event-driven trading flow with data/strategy intermediate representations for easy multi-data-interface and multi-trading-interface access. (Source: README.md:109-110, docs/DEVELOPMENT.md:3-5)
5. **Multi-Asset Support** — Supports multiple trading targets: stocks, funds, futures, and cryptocurrencies. (Source: README.md:110, docs/README.md:237)
6. **Frontend/Backend Separation** — wxPython-based GUI client + backend plugin services (fund-strategies, QInvestool, browser extension). (Source: docs/DEVELOPMENT.md:28-36, docs/README.md:183)
7. **Cross-Platform Support** — Runs on Windows, Linux, and Mac. (Source: docs/README.md:546-551, docs/Install_guide.md:11-27)
8. **Quantstats Dashboard** — Quantstats-based performance visualization and tear-sheet reports. (Source: README.md:663-667, docs/README.md:587-591)
9. **GUI Client (Desktop)** — Desktop GUI application built with wxPython, with four main windows. (Source: docs/README.md:183, docs/DEVELOPMENT.md:39)
10. **Web Extension** — Browser extension "Stock/Fund Manager" (股票基金管家) for market monitoring. (Source: docs/DEVELOPMENT.md:35)
11. **Docker Support (In Development)** — Docker-based deployment is mentioned as in development. (Source: docs/Install_guide.md:111-121)
12. **No-Code Operation with Dagster** — Dagster integration for batch processing, scheduled tasks, financial data collection, and ML workflow orchestration. (Source: README.md:718-728, docs/README.md:640-650)
13. **Jupyter Notebook Integration** — Provides Jupyter notebooks for interactive strategy analysis. (Source: docs/tutorials_code/README.md:1-41, README.md:459)
14. **Binder Support** — One-click Binder environment to run strategy notebooks in the cloud. (Source: README.md:459)
15. **DeepWiki Integration** — Integration with DeepWiki for AI-powered documentation Q&A. (Source: README.md:20, README.md:39)
16. **Online Documentation Website** — Docs deployed to GitHub Pages via docsify. (Source: README.md:19, docs/FQA.md:23)

---

## Category: Data Layer & Data Loading

17. **Multiple Data Sources** — Supports data acquisition from multiple sources (Tushare, baostock, etc.). (Source: docs/tutorials_code/README.md:39, docs/02-经典策略/01-股票/量化二-选股.md:7-8)
18. **Tushare Pro Integration** — Integration with Tushare Pro API for daily data, daily_basic indicators, stock_basic info, income data. (Source: docs/02-经典策略/01-股票/量化二-选股.md:10-16, docs/02-经典策略/01-股票/量化三-配对交易.md:16-71)
19. **Baostock Data Integration** — Free open-source securities data platform baostock integration for historical stock data. (Source: docs/tutorials_code/15.rl_learning/README.md:98-99)
20. **A-Share Historical Data** — Supports A-share (Chinese stock market) historical data including daily OHLCV, fundamentals, and more. (Source: docs/02-经典策略/01-股票/量化一-均值策略.md:9-10, docs/02-经典策略/01-股票/量化二-选股.md:7)
21. **Data Caching/Local Storage** — Data fetched once and stored locally in CSV format to avoid redundant network requests. (Source: docs/02-经典策略/01-股票/量化一-均值策略.md:51-68, docs/02-经典策略/01-股票/量化三-配对交易.md:440-468)
22. **Real-Time Data (Advertised Future)** — TODO item to enhance real-time data acquisition to per-second granularity with reduced latency. (Source: README.md:714)
23. **HK Stock Support** — Hong Kong stock data support mentioned in git commit history. (Source: git log: 4b9a963)

---

## Category: Trading Indicators & Technical Factors

24. **30+ Technical Indicators** — Supports EMA, MACD, KDJ, RSRS, RSI, StochRSI, BIAS, BOLL, OBV, SAR, VOL, PSY, ARBR, CR, BBI, EMV, TRIX, DMA, DMI, CCI, ROC, ENE, SKDJ, LWR, P/E ratio, P/B ratio, and more. (Source: README.md:498-538, docs/README.md:462-503)
25. **17 Daily Stock Indicators** — A `guess_indicators_daily` table computing Volume Delta, n-day difference, n-day change %, CR, Max/Min, KDJ, SMA, MACD, BOLL, RSI, W%R, CCI, TR/ATR, DMA, DMI/ADX/ADXR, TRIX, VR/MAVR. (Source: docs/02-经典策略/01-股票/股票指标.md:1-22)
26. **Alpha-101 & Alpha-191 Factor Sets** — Includes Alpha-101 and Alpha-191 factor libraries. (Source: README.md:497, docs/README.md:461)
27. **Automated Factor Generation (DEAP)** — Automated factor generation using DEAP (genetic programming) library. (Source: README.md:497, docs/README.md:461)
28. **1000+ Trading Factors** — Claims "thousands of trading factors" available in the platform. (Source: README.md:639)
29. **Paid/Premium Indicators** — Advertises premium indicators: Main force intention, Buy/Sell spread, Retail investor line, Intraday game, Buy/Sell force, Market trend, MTM momentum, Smart MACD/KDJ/RSI/WR parameters, Qbot AI prediction, Qbot buy/sell strength. (Source: README.md:490-502, docs/README.md:490-502)
30. **Factor Expression Engine** — Factor expression-based calculation for user-defined factors. (Source: README.md:122, README.md:651)

---

## Category: Classic Strategies (Stock/Futures/Crypto)

31. **Bollinger Band Mean Reversion** — BOLL-based mean reversion strategy with backtest results and robustness analysis. (Source: docs/02-经典策略/01-股票/布林线均值回归.md:1-113)
32. **Multi-Factor Stock Selection** — Fama-French three-factor model-based stock selection strategy. (Source: docs/02-经典策略/01-股票/多因子选股.md:1-264)
33. **Small Market Cap Strategy** — Invests in smallest market cap stocks monthly, equal-weighted. (Source: docs/02-经典策略/01-股票/小市值.md:1-158)
34. **Index Enhancement Strategy** — Alpha overlay on index tracking for excess returns. (Source: docs/02-经典策略/01-股票/指数增强.md:1-5, README.md:325)
35. **Alpha Hedging** — Market-neutral alpha hedging strategy. (Source: docs/02-经典策略/01-股票/Alpha对冲.md:1-5, README.md:331)
36. **RSRS Timing Strategy** — Resistance Support Relative Strength timing strategy. (Source: docs/02-经典策略/01-股票/量化策略-RSRS择时.md:4-7)
37. **Moving Average Crossover (SMA Cross)** — Simple dual moving average crossover strategy via backtrader. (Source: docs/02-经典策略/01-股票/量化一-均值策略.md:11-31)
38. **ARBR Sentiment Indicator Strategy** — ARBR-based sentiment trading strategy. (Source: README.md:280, README.md:304)
39. **Aroon Trend Trading** — Aroon indicator-based trend trading strategy. (Source: README.md:281, README.md:305)
40. **RSI Divergence Strategy** — RSI divergence-based trading strategy. (Source: README.md:288, README.md:312)
41. **StochRSI Strategy** — Stochastic RSI strategy. (Source: README.md:290, README.md:314)
42. **Sparrow Search Algorithm (SSA)** — SSA optimization-based trading strategy. (Source: README.md:289, README.md:313)
43. **Undervalued Stock Picking** — Market undervaluation-based stock picking strategy. (Source: README.md:292)
44. **Dual Moving Average Strategy (Klines)** — Double moving average trading strategy for futures. (Source: README.md:303, docs/02-经典策略/03-期货/双均线策略.md)
45. **Pair Trading** — Cointegration-based pair trading strategy with backtrader implementation. (Source: docs/02-经典策略/01-股票/量化三-配对交易.md:1-598)
46. **Fundamental Stock Screening** — PE/PB-based fundamental stock selection using Tushare data. (Source: docs/02-经典策略/01-股票/量化二-选股.md:1-117)

---

## Category: Combined Factor & Multi-Strategy

47. **RSI + CCI Combination Strategy** — Combined RSI and CCI indicator strategy. (Source: README.md:318)
48. **MACD + ADX Combination Strategy** — Combined MACD and ADX indicator strategy. (Source: README.md:319)
49. **MACD + KDJ Combination Strategy** — Combined MACD and KDJ strategy with backtest. (Source: README.md:320, docs/tutorials_code/README.md:17-20)
50. **Multi-Factor Trading Strategy** — Multi-factor trading strategy combining multiple indicators. (Source: README.md:321)
51. **Alphalens Factor Backtesting** — Alphalens-based multi-factor backtesting framework. (Source: README.md:322)
52. **Multi-Strategy Integration** — Integration of multiple strategies (harami pattern + others). (Source: README.md:323, docs/tutorials_code/README.md:23)
53. **Portfolio Combination Strategy** — Kurtosis Portfolio combination strategy via Jupyter notebook. (Source: README.md:324, README.md:342)
54. **Multi-Factor Auto-Combination** — Automatic multi-factor combination strategy. (Source: README.md:346)

---

## Category: AI / Machine Learning / Deep Learning Strategies

55. **LightGBM Prediction** — LightGBM-based price prediction strategy. (Source: README.md:282)
56. **SVM Prediction** — Support Vector Machine-based prediction strategy. (Source: README.md:283)
57. **LSTM Time Series Prediction** — LSTM neural network for time series price prediction. (Source: README.md:284)
58. **Reinforcement Learning Prediction** — RL-based trading strategy. (Source: README.md:285)
59. **Q-Learning Prediction** — Q-Learning algorithm for trading decisions. (Source: README.md:286)
60. **Random Forest Prediction** — Random Forest-based prediction strategy. (Source: README.md:287)
61. **XGBoost** — XGBoost benchmark model from KDD 2016. (Source: README.md:401)
62. **CatBoost** — CatBoost benchmark model from NIPS 2018. (Source: README.md:403)
63. **DoubleEnsemble** — DoubleEnsemble model from ICDM 2020. (Source: README.md:407)
64. **TabNet** — TabNet model from ECCV 2022 / AAAI 2019. (Source: README.md:408, README.md:421)
65. **Linear Regression** — Linear regression baseline model. (Source: README.md:412)
66. **MLP** — Multi-Layer Perceptron model. (Source: README.md:418)
67. **GRU** — GRU recurrent neural network model from ICCVW 2021. (Source: README.md:419)
68. **ALSTM** — Augmented LSTM from IJCAI 2022. (Source: README.md:426)
69. **ADARNN** — Adaptive Directional-Aware RNN from KDD 2021. (Source: README.md:427)
70. **ADD** — Adaptive Dual-Driven from CoRL 2020. (Source: README.md:428)
71. **KRNN** — Knowledge-based RNN. (Source: README.md:429)
72. **Sandwich Model** — Sandwich architecture model. (Source: README.md:430)
73. **TFT (Temporal Fusion Transformer)** — TFT from IJoF 2019. (Source: README.md:434)
74. **GATs (Graph Attention Networks)** — Graph Attention Networks from NIPS 2017. (Source: README.md:435)
75. **SFM (Soft Factorization Machine)** — SFM from KDD 2017. (Source: README.md:436)
76. **Transformer** — Transformer model from NeurIPS 2017. (Source: README.md:439)
77. **TCTS** — TCTS from ICML 2021. (Source: README.md:440)
78. **TRA (Temporal Relation-Aware)** — TRA from KDD 2021. (Source: README.md:441)
79. **TCN (Temporal Convolutional Network)** — TCN from KDD 2018. (Source: README.md:442)
80. **IGMTF** — IGMTF from KDD 2021. (Source: README.md:443)
81. **HIST** — HIST model. (Source: README.md:444)
82. **Localformer** — Localformer model. (Source: README.md:445)
83. **ChatGPT Integration** — ChatGPT-based strategy writing and intelligent Q&A. (Source: README.md:448, docs/Install_guide.md:155)
84. **FinGPT Integration** — FinGPT large language model integration for finance. (Source: README.md:449)
85. **300+ AI Models / 40+ Papers** — Claims support for 300+ models and methods from 40+ papers in the Model Zoo. (Source: README.md:489, docs/README.md:453)
86. **PPO Reinforcement Learning** — Proximal Policy Optimization for automated stock trading via OpenAI Gym environment. (Source: docs/tutorials_code/15.rl_learning/README.md:82)

---

## Category: Smart Trading Strategies

87. **Turning Point Trading (拐点交易)** — Buy/sell based on price drop/rise thresholds and pullback ratios. (Source: docs/03-智能策略/拐点交易.md:1-20)
88. **Grid Trading (网格交易)** — Automated position adjustment within a price range using grid parameters. (Source: docs/03-智能策略/网格交易.md:1-18)
89. **Limit-Up Opening Strategy (涨停开板策略)** — Strategy for trading limit-up stocks. (Source: docs/03-智能策略/涨停开板策略.md, docs/_sidebar.md:19)
90. **Turtle Strategy (海龟策略)** — Turtle trading strategy advertised in strategy pool. (Source: README.md:336, docs/README.md:301)
91. **Trend Trading (趋势交易)** — Trend following strategy. (Source: README.md:335, docs/README.md:300)
92. **Dynamic Balance Strategy (动态平衡策略)** — Portfolio dynamic rebalancing strategy. (Source: README.md:337, README.md:345)

---

## Category: Fund Strategies

93. **4433 Rule Fund Selection** — 4433 rule-based fund screening and evaluation. (Source: docs/02-经典策略/02-基金/4433法则.md:1, README.md:355)
94. **Fund Hedging (Index + Bond)** — Index fund + bond fund hedging strategy. (Source: README.md:361)
95. **Multi-Factor Fund Allocation** — Multi-factor combination configuration for fund allocation. (Source: README.md:362)
96. **Intelligent Fund Algorithm 1 (惠赢智能算法1)** — Proprietary intelligent fund allocation algorithm. (Source: README.md:363)
97. **Timing Multi-Strategy (择时多策略)** — Timing-based multi-strategy for funds. (Source: README.md:364)
98. **Zhiying Multi-Factor 1 (智赢多因子1)** — Multi-factor fund strategy. (Source: README.md:365)
99. **Fund Analysis Tool (fund-strategies)** — Backend plugin for fund analysis, fund evaluation, and strategy evaluation. (Source: docs/DEVELOPMENT.md:33, backend/fund-strategies/)

---

## Category: Backtesting

100. **Online Backtesting** — Web-based strategy backtesting capability. (Source: README.md:186, docs/README.md:120)
101. **Backtrader Integration** — Backtesting framework based on backtrader. (Source: README.md:64, docs/tutorials_code/README.md:39)
102. **EasyQuant Integration** — EasyQuant-based backtesting framework. (Source: README.md:64)
103. **Backtesting with Commission & Slippage** — Configurable commission and slippage ratios in backtesting. (Source: docs/02-经典策略/01-股票/量化一-均值策略.md:103-104, docs/02-经典策略/01-股票/布林线均值回归.md:90-91)
104. **Backtest Analyzers (Sharpe Ratio, Drawdown)** — Built-in analyzers for Sharpe Ratio, maximum drawdown. (Source: docs/02-经典策略/01-股票/量化一-均值策略.md:105-106)
105. **MACD Backtest Example** — Full MACD strategy backtest example with results. (Source: README.md:682-688, docs/tutorials_code/README.md:11-13)
106. **KDJ Backtest Example** — KDJ strategy backtest example. (Source: README.md:690-696, docs/tutorials_code/README.md:15-18)
107. **KDJ+MACD Combined Backtest** — Combined KDJ and MACD backtest example. (Source: README.md:698-704, docs/tutorials_code/README.md:19-20)
108. **Strategy Robustness Testing** — Varying backtest periods to test strategy stability. (Source: docs/02-经典策略/01-股票/布林线均值回归.md:102-111, docs/02-经典策略/01-股票/小市值.md:140-157)

---

## Category: Live Trading (Simulated & Real)

109. **Simulated Trading (模拟交易)** — Simulated trading with near-real-time latency and slippage simulation. (Source: README.md:82, docs/README.md:80)
110. **Automated Live Trading (实盘自动化交易)** — Fully automated live trading execution. (Source: README.md:186, docs/README.md:120)
111. **Slippage Simulation** — Simulated slippage in simulated trading environment. (Source: README.md:82)
112. **Qbot Pro Native Trading** — qbot_pro supports stocks, futures, funds, and crypto on Win/Linux/Mac. (Source: docs/README.md:546)
113. **GoldQuant Simulation (掘金仿真)** — GoldQuant simulated trading platform integration. (Source: docs/README.md:547)
114. **Polaris Quantitative Simulation (极星量化)** — Futures simulated trading. (Source: docs/README.md:548)
115. **WonderTrader Simulation** — Stock and futures simulation. (Source: docs/README.md:549)
116. **TradingView Integration** — Cryptocurrency trading via TradingView. (Source: docs/README.md:550)

---

## Category: Live Trading APIs — Futures

117. **CTP** — China Futures Trading Platform API. (Source: README.md:569)
118. **CTPMini** — CTP Mini version. (Source: README.md:570)
119. **Femas (飞马)** — Femas futures trading API. (Source: README.md:571)
120. **Ikon (艾克朗科)** — Multicast market data only. (Source: README.md:572)
121. **Yida (易达)** — Yida futures trading API. (Source: README.md:573)

---

## Category: Live Trading APIs — Options

122. **CTPOpt** — CTP Options API. (Source: README.md:576)
123. **MA Opt (金证期权)** — King证 options API. (Source: README.md:577)
124. **QWIN** — QWIN secondary development. (Source: README.md:578)

---

## Category: Live Trading APIs — Stocks

125. **Zhongtai XTP** — Zhongtai Securities XTP API. (Source: README.md:580)
126. **Zhongtai XTPXAlgo** — XTP algorithmic trading API. (Source: README.md:581)
127. **Huaxin Qidian** — Huaxin Securities Qidian API. (Source: README.md:582)
128. **Huarui ATP** — Huarui ATP trading API. (Source: README.md:583)
129. **Kuanrui OES** — Kuanrui OES API. (Source: README.md:584)
130. **Tonghuashun (同花顺)** — Tonghuashun trading client integration. (Source: README.md:585)
131. **Eastmoney (东方财富)** — Eastmoney trading API. (Source: README.md:586)
132. **Huatai Securities (华泰证券)** — Huatai Securities trading API. (Source: README.md:587)
133. **Guotai Junan (国泰君安)** — Guotai Junan trading API. (Source: README.md:588)
134. **Zhonghui Yida** — Zhonghui Yida trading API. (Source: README.md:589)
135. **Hengsheng UFT** — Hengsheng UFT API. (Source: README.md:590)
136. **JinGe (掘金)** — JinGe trading API. (Source: README.md:591)
137. **Dingdian Feichuang** — Dingdian Feichuang trading API. (Source: README.md:592)
138. **Tongdaxin (通达信)** — Tongdaxin trading client integration. (Source: README.md:593)

---

## Category: Live Trading APIs — Cryptocurrency

139. **OKEX/欧易** — OKEX exchange API. (Source: README.md:595)
140. **Binance (币安)** — Binance exchange API. (Source: README.md:596)
141. **Huobi (火币)** — Huobi exchange API. (Source: README.md:597)

---

## Category: Notification & Alert System

142. **Email Notifications** — Email alerts for trade info, daily P&L, stock recommendations. (Source: README.md:217, docs/README.md:150)
143. **Feishu (Lark) Notifications** — Feishu/Lark messaging integration. (Source: README.md:217, docs/DEVELOPMENT.md:19)
144. **System Popup Notifications** — Desktop popup alerts. (Source: README.md:217, docs/README.md:150)
145. **WeChat Notifications** — WeChat message alerts. (Source: README.md:217, docs/DEVELOPMENT.md:19)
146. **DingTalk Notifications** — DingTalk messaging integration. (Source: docs/DEVELOPMENT.md:19)
147. **Enterprise WeChat Notifications** — Enterprise WeChat (WeCom) integration. (Source: docs/DEVELOPMENT.md:19)
148. **AI Stock Recommendation Email Subscription** — Automated daily stock recommendation list delivered via email. (Source: README.md:805, docs/README.md:715)

---

## Category: Analysis & Evaluation

149. **Quantstats Integration** — Quantstats-based tear-sheet reports for performance visualization. (Source: README.md:663-667, backend/quantstats/)
150. **Indicator Analysis** — Stock indicator analysis module. (Source: docs/DEVELOPMENT.md:21)
151. **Algorithm Library (算子库)** — Algorithm/operator library for quantitative analysis. (Source: docs/DEVELOPMENT.md:21)
152. **Evaluation Result Analysis** — Backtest result evaluation and analysis. (Source: docs/DEVELOPMENT.md:21)
153. **Stock/Fund Evaluation** — Stock and fund evaluation tools via QInvestool. (Source: docs/DEVELOPMENT.md:34)
154. **Factor Mining** — Automated factor mining capabilities. (Source: docs/DEVELOPMENT.md:34)

---

## Category: Risk Control & Portfolio Management

155. **Portfolio Risk Control** — Risk control via position management and combination optimization. (Source: README.md:269, docs/README.md:232)
156. **Industry Neutral** — Industry neutral constraint in index enhancement. (Source: docs/01-新手指引/量化策略的分类和原理.md:269)
157. **Style Neutral** — Style neutral constraint for tracking. (Source: docs/01-新手指引/量化策略的分类和原理.md:269)
158. **Position Sizing** — Configurable position sizes and allocation. (Source: README.md:269, docs/02-经典策略/01-股票/小市值.md:100)
159. **Commission Configuration** — Configurable commission rates for backtesting. (Source: README.md:679)

---

## Category: Stock Selection Tools

160. **AI Stock Selection (Smart Stock Picking)** — AI-powered stock selection. (Source: docs/Install_guide.md:158)
161. **AI Stock Evaluation (Smart Stock Analysis)** — AI-powered stock analysis/evaluation. (Source: docs/Install_guide.md:158)
162. **QInvestool** — Go-based stock/fund evaluation, stock selection, and factor mining tool. (Source: docs/DEVELOPMENT.md:34)

---

## Category: CI/CD & DevOps

163. **CodeQL Analysis** — GitHub Actions CodeQL security analysis. (Source: README.md:14, docs/README.md:14)
164. **Auto-Trade Workflow** — Automated trading CI/CD workflow via GitHub Actions. (Source: README.md:15, docs/README.md:15)
165. **Pylint Linting** — Automated code linting with Pylint. (Source: README.md:16, docs/README.md:16)
166. **Coverage Testing** — Automated code coverage testing. (Source: README.md:17, docs/README.md:17)

---

## Category: Qbot Pro (Paid Version) Features

167. **Qbot Pro Full Closed-Loop** — AI stock selection, data acquisition/cleaning, strategy development, backtesting, simulated trading, live automated trading. (Source: README.md:651)
168. **Encapsulated API Examples** — Ready-to-use API examples and system source code development examples. (Source: README.md:651)
169. **Strategy Templates & Factor Expressions** — Easy-to-use strategy templates and factor expression templates. (Source: README.md:651)
170. **Quantitative Trading Think Tank** — Research report reproduction, cutting-edge strategy exploration, investment research information. (Source: README.md:651)
171. **Community Support** — Community-based Q&A service. (Source: README.md:651)
172. **VIP Version** — One-on-one service, latest quantitative trading system, packaged fund/stock/futures/crypto interfaces, multiple intelligent strategy examples, remote technical support. (Source: README.md:652)

---

## Category: Developer & Community Features

173. **Open Source (CC BY-NC-SA 4.0)** — Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0. (Source: README.md:844, docs/README.md:746)
174. **Knowledge Planet Community** — Paid community for strategy sharing, live trading tutorials, real-time data interfaces. (Source: README.md:753-754, docs/README.md:665)
175. **WeChat Mini Program** — Qbot WeChat mini program in development. (Source: README.md:72, docs/README.md:70)
176. **GitHub Discussions & Issues** — Community support via GitHub. (Source: README.md:746-747)
177. **Contributor Recognition** — Top 10 contributors get 1-year free access; top 3 get lifetime free Pro access. (Source: README.md:644, docs/README.md:579)
178. **Strategy Service Marketplace** — Community-contributed strategies can be provided as services for revenue. (Source: README.md:636-639, docs/README.md:571-573)

---

## Category: Educational Content

179. **Quantitative Strategy Classification & Principles** — Comprehensive guide to quantitative strategy types and theory. (Source: docs/01-新手指引/量化策略的分类和原理.md:1-600)
180. **15+ Tutorial Code Examples** — Practical tutorial code for backtrader, MACD, KDJ, RF, RL, alphalens, Qlib, etc. (Source: docs/tutorials_code/README.md:1-41)
181. **Beginner-Friendly Documentation** — Detailed strategy principles and platform setup guides. (Source: README.md:659, docs/README.md:583)
182. **Online Documentation Website** — Full docs deployed at ufund-me.github.io/Qbot. (Source: README.md:33, README.md:661)

---

## Category: Exchange-Specific Broker Client Support

183. **Haitong Securities Client** — Haitong online trading system integration. (Source: README.md:557)
184. **Huatai Securities Client** — Huatai professional trading platform integration. (Source: README.md:558)
185. **Guojin Securities Client** — Guojin all-around securities trading terminal. (Source: README.md:559)
186. **Generic Tonghuashun Client** — Generic Tonghuashun client requiring manual login. (Source: README.md:559)

---

## Summary Statistics

| Category | Feature Count |
|---|---|
| Platform Overview & Architecture | 16 |
| Data Layer & Data Loading | 7 |
| Trading Indicators & Technical Factors | 7 |
| Classic Strategies | 16 |
| Combined Factor & Multi-Strategy | 8 |
| AI / ML / DL Strategies | 32 |
| Smart Trading Strategies | 6 |
| Fund Strategies | 7 |
| Backtesting | 9 |
| Live Trading (Simulated & Real) | 8 |
| Live Trading APIs (Futures/Options/Stocks/Crypto) | 25 |
| Notification & Alert System | 7 |
| Analysis & Evaluation | 6 |
| Risk Control & Portfolio Management | 5 |
| Stock Selection Tools | 3 |
| CI/CD & DevOps | 4 |
| Qbot Pro (Paid Version) | 6 |
| Developer & Community Features | 6 |
| Educational Content | 4 |
| Broker Client Support | 4 |
| **TOTAL** | **186** |

---

## Category: Additional Features Found in Source Code, Workflows & Config

> These features were discovered from deeper inspection of setup.py, requirements.txt, GitHub Actions workflows, GUI mainframe source, trading engine code, and source comments — not found in docs/ or README.md.

### GUI Application Tabs (Source: qbot/gui/mainframe.py:125-151)

187. **Qbot Research Think Tank (投研智库) Tab** — Dedicated tab with research reports served via local HTTP server on port 9080. (Source: qbot/gui/mainframe.py:125, qbot/gui/panels/panel_zhiku.py:44-58)
188. **ChatGPT Strategy Writing Tab** — Web panel tab embedding a ChatGPT-powered strategy writing interface at aitianhu.com. (Source: qbot/gui/mainframe.py:127-129)
189. **AI Stock/Fund Selection Tab** — Web panel for AI-powered stock/fund picking hosted at external server. (Source: qbot/gui/mainframe.py:131-133)
190. **Fund Investment Strategy Analysis Tab** — Web panel for fund strategy analysis hosted at GitHub Pages. (Source: qbot/gui/mainframe.py:135-137)
191. **Visual Stock/Fund Backtesting System Tab** — Native wxPython panel with full backtest configuration UI (strategy selection, date range, benchmark, commission, slippage). Set as default home tab. (Source: qbot/gui/mainframe.py:141, qbot/gui/panels/panel_backtest.py:53-80)
192. **Online Trading Tab (Real/Virtual)** — Combined panel with simulated trading and live trading sub-tabs, using 东方财富 as platform. (Source: qbot/gui/mainframe.py:149, qbot/gui/panels/panel_trade.py:12-47)
193. **Scheduled Auto-Trading (Cron)** — Commented-out tab for "交易策略在线交易" pointing to GoldQuant simulation. (Source: qbot/gui/mainframe.py:143-145)
194. **User/Action Panel (Commented Out)** — Commented-out tabs for UserFrame and ActionsPanel (asset rotation strategy analysis). (Source: qbot/gui/mainframe.py:147-148)
195. **Conditional Stock Picking Panel (条件选股)** — Commented-out sub-panel for condition-based stock screening. (Source: qbot/gui/panels/panel_backtest.py:151,162)
196. **Pattern Stock Picking Panel (形态选股)** — Commented-out sub-panel for pattern-based stock screening. (Source: qbot/gui/panels/panel_backtest.py:152,163)

### GUI Tools Menu (Source: qbot/gui/mainframe.py:51-63)

197. **Danjuan Valuation Tool (蛋卷估值)** — Menu item opening Danjuan app valuation center in web browser. (Source: qbot/gui/mainframe.py:54-56)
198. **Jisilu Data Tool (集思录)** — Menu item opening Jisilu.cn financial data platform. (Source: qbot/gui/mainframe.py:58-60)
199. **Background Monitoring (后台监控)** — Menu item to start stock price monitoring via auto_monitor.py script. (Source: qbot/gui/mainframe.py:61-63, qbot/gui/mainframe.py:107-113)
200. **Parameter Configuration Dialog** — Settings menu for API key/secret configuration for trading platforms. (Source: qbot/gui/mainframe.py:46-49)

### Backtesting Panel Features (Source: qbot/gui/panels/panel_backtest.py)

201. **Stock/Futures/Bitcoin Trading Target Input** — Input field supporting stock codes, futures, and Bitcoin. (Source: qbot/gui/panels/panel_backtest.py:218)
202. **Kline Chart Display (pyecharts)** — Real-time Kline and line charts using pyecharts library. (Source: qbot/gui/panels/panel_backtest.py:34-35)
203. **Benchmark Selection** — Dropdown for benchmark selection including 沪深300指数 and S&P 500. (Source: qbot/gui/panels/panel_backtest.py:128-129, 376)
204. **Configurable Commission, Slippage, Stamp Duty, Min Cost** — Full trade cost configuration in backtest UI. (Source: qbot/gui/panels/panel_backtest.py:65-76)
205. **Trade Log Viewer** — Button to view trading logs. (Source: qbot/gui/panels/panel_backtest.py:500-501)
206. **Akshare Data Integration** — Using akshare for real-time stock data in backtest panel. (Source: qbot/gui/panels/panel_backtest.py:29)

### Registered Backtest Strategies in GUI (Source: qbot/gui/panels/panel_backtest.py:39-45)

207. **RSI Strategy** — "单因子-相对强弱指数RSI" registered as default strategy. (Source: qbot/gui/panels/panel_backtest.py:40)
208. **SMA Cross Strategy** — "单因子-简单移动均线" registered in strategy dropdown. (Source: qbot/gui/panels/panel_backtest.py:41)
209. **Boll Strategy** — "单因子-布林线均值回归" registered in strategy dropdown. (Source: qbot/gui/panels/panel_backtest.py:42)
210. **SSA Strategy** — "机器学习-麻雀优化算法SSA" registered in strategy dropdown. (Source: qbot/gui/panels/panel_backtest.py:43)
211. **Multi-Strategy** — "多因子-ROC(20)动量信号周频Top1" registered in strategy dropdown. (Source: qbot/gui/panels/panel_backtest.py:44)

### Simulated & Real Trading Panel Features (Source: qbot/gui/panels/panel_trade.py)

212. **Simulated Trading Sub-Tab** — Using 东方财富 as platform with stock trading via RSI strategy. (Source: qbot/gui/panels/panel_trade.py:25-32)
213. **Real Trading Sub-Tab** — Live trading with 东方财富 platform and stock trading via RSI strategy. (Source: qbot/gui/panels/panel_trade.py:34-43)
214. **Focus Stock List (Commented Out)** — "我的自选(预留)" placeholder for watchlist feature. (Source: qbot/gui/panels/panel_trade.py:9,23)

### Auto Monitoring Features (Source: qbot/plugins/auto_monitor.py)

215. **Real-time Stock Price Monitoring** — Continuous loop checking stock prices against thresholds. (Source: qbot/plugins/auto_monitor.py:123-158)
216. **Feishu/Lark Webhook Alerts** — Sends trade signals via Feishu/Lark Bot webhook. (Source: qbot/plugins/auto_monitor.py:32, 125, 127)
217. **Mac Native Notifications (pync)** — macOS system notifications via pync library. (Source: qbot/plugins/auto_monitor.py:28, 131-136)
218. **macOS Sound Alerts** — Audio bell sound (bell.wav) on price threshold triggers. (Source: qbot/plugins/auto_monitor.py:121, 155)
219. **Cron-Based Scheduled Monitoring** — Designed to run via crontab every 3 minutes during trading hours (Mon-Fri 9-12, 13-15). (Source: qbot/plugins/auto_monitor.py:58-64)
220. **Customizable Stock Pool with Thresholds** — Configurable stocks pool with min/max price thresholds for alerts. (Source: qbot/plugins/auto_monitor.py:66-70)

### Dagster Pipeline Features (Source: qbot/plugins/dagster/dagster_taskgraph.py)

221. **Bond Factor Pipeline** — Dagster job for loading bond lists from MongoDB, updating factors, and merging data. (Source: qbot/plugins/dagster/dagster_taskgraph.py:1-50)

### Bitcoin Arbitrage Trading (Source: qbot/engine/trade/trading/bitcoin-arbitrage/)

222. **Cross-Exchange Bitcoin Arbitrage** — Bitcoin arbitrage trading system with observer pattern. (Source: qbot/engine/trade/trading/bitcoin-arbitrage/)
223. **Email Trade Alerts** — Email notification observer for arbitrage opportunities. (Source: qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/emailer.py:8, 27)
224. **XMPP Messaging Alerts** — XMPP-based real-time messaging for trade signals. (Source: qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/xmppmessager.py:24-26)
225. **Specialized Trader Bot** — Specialized trader bot with email integration. (Source: qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/specializedtraderbot.py:5, 112)

### Tonghuashun (THS) Auto-Trading (Source: qbot/engine/trade/trading/thsauto/)

226. **THS Balance Query** — Account balance query via Tonghuashun. (Source: qbot/engine/trade/trading/thsauto/server.py:50)
227. **THS Position Query** — Current position query. (Source: qbot/engine/trade/trading/thsauto/server.py:58)
228. **THS Active Orders Query** — Active orders query. (Source: qbot/engine/trade/trading/thsauto/server.py:66)
229. **THS Filled Orders Query** — Historical filled orders query. (Source: qbot/engine/trade/trading/thsauto/server.py:74)
230. **THS Automated Sell** — Automated sell order execution. (Source: qbot/engine/trade/trading/thsauto/server.py:82)
231. **THS Automated Buy** — Automated buy order execution. (Source: qbot/engine/trade/trading/thsauto/server.py:95)
232. **THS Science Board Buy (buy_kc)** — Automated buy for 科创板 (STAR Market). (Source: qbot/engine/trade/trading/thsauto/server.py:108)
233. **THS Scheduled Interval Trading** — Interval-based scheduled order execution. (Source: qbot/engine/trade/trading/thsauto/server.py:27)

### EmQuant API Integration (Source: qbot/engine/trade/trading/emt_api/)

234. **EmQuantAPI Installation Tool** — Helper for installing EmQuant API. (Source: qbot/engine/trade/trading/emt_api/installEmQuantAPI.py:9)
235. **EmQuant Market Data Callbacks** — Real-time market data callbacks (main, start, CSQ, CST, CNQ). (Source: qbot/engine/trade/trading/emt_api/demo.py:12-79)
236. **EmQuant C-Extension Types** — Low-level C extension types for data handling. (Source: qbot/engine/trade/trading/emt_api/EmQuantAPI.py:63-86)

### EasyTrader Integration (Source: requirements/dev/requirements.txt, qbot/engine/trade/easytrader/)

237. **EasyTrader Broker Client Control** — Automates broker client operations via easytrader library. (Source: dev/requirements.txt:9)
238. **EasyQuotation Real-time Quotes** — Real-time stock quotation via easyquotation. (Source: dev/requirements.txt:11)

### QMT/PTrade Broker Support (Source: qbot/engine/trade/engine_apis/venv/README.md)

239. **76+ Broker QMT/PTrade Support** — Comprehensive table of 76+ brokers supporting QMT/PTrade quantitative trading platforms. (Source: qbot/engine/trade/engine_apis/venv/README.md:97-187)
240. **Broker Test Accounts** — Test account access for 国金证券, 国盛证券, 华泰证券 (QMT/PTrade). (Source: qbot/engine/trade/engine_apis/venv/README.md:36-90)

### Package Dependencies (Advertised Capabilities via requirements.txt)

241. **Binance Connector** — Official Binance API connector for cryptocurrency trading. (Source: requirements.txt:12)
242. **yfinance** — Yahoo Finance data integration for global stock data. (Source: requirements.txt:26)
243. **efinance** — Eastmoney finance data integration. (Source: requirements.txt:27)
244. **akshare** — AkShare financial data API for Chinese market data. (Source: requirements.txt:28)
245. **pandas_datareader** — Multi-source data reader (FRED, World Bank, Yahoo, etc.). (Source: requirements.txt:29)
246. **baostock** — Free A-share securities data from baostock. (Source: pytrader/requirements.txt:29)
247. **TensorTrade** — Reinforcement learning trading environment. (Source: requirements.txt:25)
248. **PyKalman** — Kalman filter for financial signal processing. (Source: requirements.txt:16)
249. **Empyrical** — Portfolio risk/performance metrics library. (Source: requirements.txt:20)
250. **Pyfolio** — Portfolio analytics and tear-sheet visualization (from quantopian). (Source: requirements.txt:5)
251. **Backtrader Plotting** — Visual backtesting chart generation. (Source: requirements.txt:6)
252. **ddddocr (OCR)** — CAPTCHA OCR recognition for automated login. (Source: dev/requirements.txt:16)
253. **jqdatasdk** — JoinQuant data SDK integration. (Source: dev/requirements.txt:17)
254. **TensorBoard** — ML training visualization via TensorBoard. (Source: requirements.txt:24)
255. **scikit-learn** — Machine learning toolkit for strategy models. (Source: requirements.txt:19)
256. **tushare** — Tushare financial data API (dev dependency). (Source: dev/requirements.txt:13)
257. **easyquotation** — Real-time stock quotation service. (Source: dev/requirements.txt:11)

### CI/CD & DevOps (Additional from Workflows)

258. **SonarCloud Static Analysis** — SonarCloud integration for continuous code quality analysis. (Source: .github/workflows/sonarqube-scan.yml:1-34)
259. **flake8 Linting** — Automated Python linting with flake8 in CI. (Source: .github/workflows/python-app.yml:34-38)
260. **mypy Static Type Checking** — Static type checking for codebase. (Source: .github/workflows/python-app.yml:41-44)
261. **nbqa (Notebook QA)** — Pylint and Black checking for Jupyter notebooks. (Source: .github/workflows/python-app.yml:48-49)
262. **PyInstaller Build** — Packaging Qbot as standalone executables for Win/Mac/Linux. (Source: .github/workflows/qbot-release.yml:196-251)
263. **GitHub Pages Auto-Deploy** — Automated documentation deployment to GitHub Pages. (Source: .github/workflows/html-static.yml:1-43)
264. **Multi-Platform Release Build** — Release pipeline builds for Ubuntu, macOS, and Windows. (Source: .github/workflows/qbot-release.yml:196-251)
265. **Investool Go Binary Release** — Cross-platform Go binary builds for investool (Mac/Linux/Win). (Source: .github/workflows/qbot-release.yml:95-155)
266. **Fund-Strategy NPM Build** — Node.js build pipeline for fund-strategies web tool. (Source: .github/workflows/qbot-release.yml:21-60)
267. **SMS Notification (Plivo)** — SMS alerts via Plivo integration in auto-trade workflow. (Source: .github/workflows/auto-trade.yml:52-59)
268. **Scheduled Auto-Trade via GitHub Actions** — Cron-based automated trading execution on trade days (hourly + Mon/Fri 9:25, 13:00, 13:15). (Source: .github/workflows/auto-trade.yml:16-21)
269. **National Holiday Skip** — Logic to skip trading on weekends and national holidays. (Source: .github/workflows/auto-trade.yml:40-44)
270. **Qlib Workflow CLI Testing** — Testing ML workflows via YAML config files (LightGBM Alpha158). (Source: .github/workflows/python-app.yml:61-64)
271. **Jupyter Notebook CI Testing** — Automated notebook execution testing. (Source: .github/workflows/python-app.py:57-59)
272. **Repo Statistics Tracking** — Automated repository clone/download/star statistics. (Source: .github/workflows/repo-stats.yml, repo-clone-stats.yml)
273. **New Contributor Greetings** — Automated welcome messages for new contributors. (Source: .github/workflows/greetings.yml)
274. **Issue/PR Labeling** — Automated label management for issues and PRs. (Source: .github/workflows/labeler.yml, tagging.yml)

### Setup.py Advertised Metadata (Source: qbot/setup.py)

275. **PyPI Package (qbot)** — Published as `qbot` Python package. (Source: qbot/setup.py:29)
276. **Console Script Entry Point** — `sample` console command entry point. (Source: qbot/setup.py:66-68)
277. **Apache License (setup.py)** — Setup.py declares Apache License (differs from README's CC BY-NC-SA 4.0). (Source: qbot/setup.py:37)

### Fund Backend (pyfunds/)

278. **xalpha Fund Library** — Fund investment toolkit (v0.11.7) with XLRD, pyecharts, SQLAlchemy, SOCKS5 proxy. (Source: pyfunds/backtest/setup.py:17-47)
279. **fund-strategies Web Tool** — Node.js-based fund strategy analysis web application. (Source: pyfunds/fund-strategies/, .github/workflows/qbot-release.yml:45-60)
280. **Coffeelings Fund Tool** — Additional fund analysis tool. (Source: pyfunds/coffeelings/)
281. **Web Browser Extension (Stock/Fund Manager)** — Chrome extension for stock/fund management. (Source: pyfunds/web-extension/)

### CTP Futures Integration (pyfutures/)

282. **CTP Futures Trading** — CTP (Comprehensive Transaction Platform) integration for futures trading. (Source: pyfutures/ctp/)
283. **CTP Ta-Lib Integration** — Technical Analysis Library integration within CTP module. (Source: pyfutures/ctp/talib/)

### VnPy Integration (Source: qbot/vnpy/)

284. **VnPy Framework** — VnPy quantitative trading framework integration directory. (Source: qbot/vnpy/)

---

## Updated Summary Statistics

| Category | Feature Count |
|---|---|
| Platform Overview & Architecture | 16 |
| Data Layer & Data Loading | 7 |
| Trading Indicators & Technical Factors | 7 |
| Classic Strategies | 16 |
| Combined Factor & Multi-Strategy | 8 |
| AI / ML / DL Strategies | 32 |
| Smart Trading Strategies | 6 |
| Fund Strategies | 7 |
| Backtesting | 9 |
| Live Trading (Simulated & Real) | 8 |
| Live Trading APIs (Futures/Options/Stocks/Crypto) | 25 |
| Notification & Alert System | 7 |
| Analysis & Evaluation | 6 |
| Risk Control & Portfolio Management | 5 |
| Stock Selection Tools | 3 |
| CI/CD & DevOps | 4 |
| Qbot Pro (Paid Version) | 6 |
| Developer & Community Features | 6 |
| Educational Content | 4 |
| Broker Client Support | 4 |
| **GUI Application Tabs & Panels** | **10** |
| **GUI Tools & Configuration** | **4** |
| **Registered Backtest Strategies** | **5** |
| **Simulated/Real Trading Panel** | **3** |
| **Auto Monitoring** | **6** |
| **Dagster Pipeline** | **1** |
| **Bitcoin Arbitrage** | **4** |
| **Tonghuashun Auto-Trading** | **8** |
| **EmQuant API** | **3** |
| **EasyTrader/EasyQuotation** | **2** |
| **QMT/PTrade Broker Support** | **2** |
| **Package Dependencies (Capabilities)** | **17** |
| **CI/CD & DevOps (Additional)** | **17** |
| **Setup.py Metadata** | **3** |
| **Fund Backend (pyfunds)** | **4** |
| **CTP Futures** | **2** |
| **VnPy Integration** | **1** |
| **TOTAL** | **284** |

---

## Discrepancies Noted

1. **License Mismatch**: README.md and docs claim CC BY-NC-SA 4.0, but `qbot/setup.py:37` declares Apache License.
2. **Missing backend/**: README.md and docs reference `backend/` directory extensively (investool, fund-strategies, web-extension, pytrader strategies), but this directory does not exist at the repo root. The actual content is at `pyfunds/`, `pytrader/`, and `qbot/plugins/investool/`.
3. **Commented-Out Features**: Several GUI features are commented out in mainframe.py — conditional stock picking (条件选股), pattern stock picking (形态选股), online strategy trading tab, user frame, and asset rotation panel. These are listed in the codebase but not functional.
4. **Missing notify/ directory**: docs/DEVELOPMENT.md:19 references `qbot/notify/` for notification implementations, but this directory does not exist.
5. **Missing data/ and analyser/ implementation**: docs/DEVELOPMENT.md references `qbot/data/` and `qbot/analyser/` for data layer and analysis layer, but these appear to be stub/empty directories.
6. **Missing engine/indicator/ and engine/algo/**: docs/DEVELOPMENT.md:21 references indicator and algorithm libraries, but these directories may not contain advertised functionality.
