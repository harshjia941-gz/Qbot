# Qbot GUI Codebase Audit Report

**Date:** 2026-05-14
**Scope:** All Python files under `qbot/gui/`
**Files scanned:** 20

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | 12    |
| MEDIUM   | 17    |
| LOW      | 11    |

---

## HIGH Severity — Core features are stubs or non-functional

### H1. `mainframe.py:107-113` — `start_monitoring` has inverted logic (kills PIDs when none exist)

**Pattern:** Stub/broken logic
**Code:**
```python
def start_monitoring(self, event):
    monitor_pids = grep_pid("monitoring")
    if not monitor_pids:          # <-- condition is INVERTED
        for pid in monitor_pids:  # <-- this loop NEVER executes
            os.system(f"kill -9 {pid}")
    os.system("nohup python qbot/plugins/auto_monitor.py > monitoring.log &")
    wx.MessageBox("股票监控程序已开启，后台查看日志。 'tail -f monitoring.log' ")
```
**What it blocks:** The monitoring kill logic never runs (condition is inverted — `if not monitor_pids` enters when list is empty, then loops over nothing). The function also references `grep_pid()` which is **not imported anywhere** — this will raise a `NameError` at runtime.
**Impact:** The entire "后台监控" menu item is broken.

---

### H2. `mainframe.py:139-141` — Startup performance TODO; no multithreading for tab loading

**Pattern:** TODO
**Code:**
```python
# TODO(Charmve):
# 多线程实现提高系统启动速度
self.tabs.AddPage(PanelBacktest(self.tabs), "可视化股票/基金回测系统", True)
```
**What it blocks:** App startup blocks on PanelBacktest init (loads UI synchronously). All tabs including heavy web panels are loaded before the window shows.

---

### H3. `mainframe.py:143-148` — Commented-out panels: UserFrame, ActionsPanel, online trading

**Pattern:** Commented-out features
**Code:**
```python
# web4 = WebPanel(self.tabs)
# self.tabs.AddPage(web4, "交易策略在线交易", True)
# web4.show_url("https://sim.myquant.cn/sim?acc=5e4cdda3-f2fb-11ed-ae27-00163e022aa6")
# self.tabs.AddPage(UserFrame(self.tabs), "Qbot 量化投研", True)
# self.tabs.AddPage(ActionsPanel(self.tabs), "资产轮动策略分析", True)
```
**What it blocks:** "交易策略在线交易", "Qbot 量化投研", and "资产轮动策略分析" tabs are disabled. Imports at the top are also commented out (lines 14-17).

---

### H4. `mainframe.py:131-133` — Hardcoded external server URLs for AI features

**Pattern:** Hardcoded placeholder / external dependency
**Code:**
```python
web2 = WebPanel(self.tabs)
self.tabs.AddPage(web2, "AI 选股/选基", True)
web2.show_url("http://111.229.117.200:4868")  # <-- hardcoded IP
```
**What it blocks:** "AI 选股/选基" feature depends on a single hardcoded IP address. If the server is down, the feature is useless. The "ChatGPT 策略编写" tab (line 129) also points to an external third-party URL (`https://wo2qwg.aitianhu.com/`).

---

### H5. `def_dialog.py:628` and `def_dialog.py:695` — WeChat contact paywall for trading API access

**Pattern:** 微信 / 联系 / paywall
**Code (line 628):**
```python
back_info = MessageDialog(f"微信联系Yida_Zhang2 获取自动化实盘交易接口后，填写参数：")
```
**Code (line 695):**
```python
back_info = MessageDialog(
    f"微信联系Yida_Zhang2 或者自行获取{trade_plat}账户uid后，填写参数."
)
```
**What it blocks:** Stock and crypto trading platform API key setup requires contacting the author via WeChat. There is no self-service way to configure trading. This is a **soft paywall/contact wall** that gates core trading functionality.

---

### H6. `panel_sim_trade.py:487` and `panel_real_trade.py:488` — WeChat contact paywall for unsupported platforms

**Pattern:** 微信 / 联系 / paywall
**Code (panel_sim_trade.py:487):**
```python
MessageDialog("交易平台尚未接入，请联系微信：Yida_Zhang2")
```
**Code (panel_real_trade.py:488):**
```python
MessageDialog("交易平台尚未接入，请联系微信：Yida_Zhang2")
```
**What it blocks:** When users select "基金" (funds) or other unsupported trade types, they get a WeChat contact prompt instead of any functionality. Futures and fund trading are non-functional.

---

### H7. `panel_backtest.py:563-569` — `_ev_enter_stcode` references undefined `self.code_table`

**Pattern:** Broken reference / stub
**Code:**
```python
def _ev_enter_stcode(self, event):
    st_code = self.stock_code_input.GetValue()
    st_name = self.code_table.get_name(st_code)  # <-- self.code_table never defined
    self.backtest_opts["code"] = st_code
```
**What it blocks:** Pressing Enter in the stock code input will crash with `AttributeError`. The `code_table` attribute is never set up (commented out in `init_ui`).

---

### H8. `panel_results.py:21` — Import of non-existent `widgets.widgets` module

**Pattern:** Broken import
**Code:**
```python
from qbot.gui.widgets.widgets import MatplotlibPanel, PandasGrid
```
**What it blocks:** `ResultsPanel` cannot be instantiated. The file `qbot/gui/widgets/widgets.py` does not exist. This panel is currently unused (not imported anywhere in the active GUI), but it is completely dead code.

---

### H9. `mainframe.py:71-76` — `on_menu` handler silently ignores unhandled menu IDs

**Pattern:** Event handler that doesn't connect to real functionality
**Code:**
```python
def on_menu(self, event):
    web = WebPanel(self.tabs)
    if event.Id == 1:
        web.show_url("https://danjuanapp.com/djmodule/value-center")
    if event.Id == 2:
        web.show_url("https://www.jisilu.cn/")
```
**What it blocks:** The handler only checks for IDs 1 and 2 ("蛋卷估值" and "集思录"). If additional menu items are ever added to the "工具" menu, they would silently do nothing. More importantly, the handler creates a new `WebPanel` every time but **never adds it as a tab** — the `web` variable is local and gets garbage collected. This means clicking these menu items does nothing visible at runtime.
**Impact:** Both "蛋卷估值" and "集思录" menu items are **non-functional** — they create orphaned panels that are never shown.

---

### H10. `def_dialog.py:45-61` — `WebDialog` class is defined but never instantiated

**Pattern:** Dialog class defined but never instantiated
**Code:**
```python
class WebDialog(wx.Dialog):  # user-defined
    def __init__(self, parent, title="Web显示", file_name="treemap_base.html", size=(1200, 900)):
        ...
```
**What it blocks:** `WebDialog` is never imported or used anywhere in the codebase. It appears to be a legacy dialog for displaying treemap HTML files.

---

### H11. `def_dialog.py:63-83` — `InputsDialog` class is defined but never instantiated

**Pattern:** Dialog class defined but never instantiated
**Code:**
```python
class InputsDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        ...
```
**What it blocks:** `InputsDialog` is never imported or used. It appears to be a predecessor to `InputDialogTwoParameters`.

---

### H12. `panel_results.py:23-166` — `ResultsPanel` is dead code; never instantiated in the active GUI

**Pattern:** Panel class defined but never instantiated
**Code:**
```python
class ResultsPanel(wx.Panel):
    def __init__(self, parent):
        super(ResultsPanel, self).__init__(parent)
        self.init_tabs()
```
**What it blocks:** `ResultsPanel` is not imported or used by `mainframe.py` or any other active panel. Combined with the broken import (H8), this entire file is dead code that would crash if ever enabled.

---

## MEDIUM Severity — Partial implementations

### M1. `panel_backtest.py:502` — Trade log button has no event binding

**Pattern:** Button handler not connected
**Code:**
```python
self.trade_log_but = wx.Button(sub_panel, -1, "交易日志")
# self.trade_log_but.Bind(wx.EVT_BUTTON, self._ev_trade_log)  # 绑定事件
```
**What it blocks:** The "交易日志" button does nothing when clicked. The handler `_ev_trade_log` (line 626) exists but is a bare `pass`.

---

### M2. `panel_backtest.py:626-627` — `_ev_trade_log` is empty

**Pattern:** Bare pass / empty function body
**Code:**
```python
def _ev_trade_log(self, event):
    pass
```
**What it blocks:** Trade log viewing feature is non-functional.

---

### M3. `panel_backtest.py:157-163` — Commented-out "条件选股" and "形态选股" tabs

**Pattern:** Commented-out features
**Code:**
```python
# self.ParaPtPanel.SetSizer(self.add_pick_para_lay(self.ParaPtPanel))
# self.ParaPaPanel.SetSizer(self.add_patten_para_lay(self.ParaPaPanel))
# self.ParaNoteb.AddPage(self.ParaPtPanel, "条件选股")
# self.ParaNoteb.AddPage(self.ParaPaPanel, "形态选股")
```
**What it blocks:** Condition-based stock picking and pattern-based stock picking tabs are disabled.

---

### M4. `panel_backtest.py:293-311` — Multi-chart display and portfolio analysis comboboxes not bound

**Pattern:** Button/menu handlers that don't connect to real functionality
**Code:**
```python
# self.pick_graph_cbox.Bind(wx.EVT_COMBOBOX, self._ev_select_graph)
...
# self.group_analy_cmbo.Bind(wx.EVT_COMBOBOX, self._ev_group_analy)
```
**What it blocks:** "多子图显示" and "投资组合分析" dropdowns are visible but do nothing when changed.

---

### M5. `panel_backtest.py:405-406, 418, 433, 448, 461` — Backtest parameter input fields not bound

**Pattern:** Unused event handlers defined but never connected
**Code:**
```python
# self.Bind(wx.EVT_TEXT, self._on_init_cash_changed, self.init_cash_input)
# self.Bind(wx.EVT_TEXT, self._on_stake_changed, self.init_stake_input)
# self.Bind(wx.EVT_TEXT, self._on_slippage_changed, self.init_slippage_input)
# self.Bind(wx.EVT_TEXT, self._on_commission_changed, self.init_commission_input)
# self.Bind(wx.EVT_TEXT, self._on_stamp_duty_changed, self.init_tax_input)
```
**What it blocks:** Users can type values into init_cash, stake, slippage, commission, and stamp_duty fields, but the UI does not react to changes. The `StartBacktest` method reads from the input fields directly, so the values are used, but there is no real-time validation or feedback.

---

### M6. `panel_backtest.py:49-51` — Unused stub function `OnBkt`

**Pattern:** Stub function
**Code:**
```python
def OnBkt(event):
    wx.MessageBox("ok")
```
**What it blocks:** Nothing (it's unused), but it indicates incomplete refactoring.

---

### M7. `panel_sim_trade.py:421-423` and `panel_real_trade.py:422-424` — Commented-out WeChat paywall in OnClickTrade

**Pattern:** Commented-out paywall (previously active)
**Code:**
```python
def OnClickTrade(self, event):
    # MessageDialog("请联系微信：Yida_Zhang2")
```
**What it blocks:** The comment suggests trading was previously gated behind a WeChat contact wall. The current code proceeds to call `TradeEngine`, but the engine may itself be a stub.

---

### M8. `panel_sim_trade.py:437-443` and `panel_real_trade.py:438-444` — Hardcoded trade options ignore user selections

**Pattern:** Hardcoded placeholder data
**Code:**
```python
sim_trade_opts = {
    "class": "虚拟盘",
    "platform": "东方财富",
    "trade_type": "股票",
    "trade_code": "399006.SZ",
    "strategy": "单因子-相对强弱指数RSI",
}
# ... then uses self.trader_opts which reflects user selection
```
**What it blocks:** The `sim_trade_opts` dict is created but never used — the code uses `self.trader_opts` instead. The dead `sim_trade_opts` variable is misleading and suggests incomplete refactoring. Same pattern in `panel_real_trade.py` where `class` is hardcoded to "实盘" in the dead variable.

---

### M9. `panel_sim_trade.py:151-158` and `panel_real_trade.py:153-159` — Stock pool double-click handler does nothing

**Pattern:** Empty handler
**Code:**
```python
def _ev_click_plcode(self, event):
    st_code = self.grid_pl.GetCellValue(event.GetRow(), 1)
    st_name = self.grid_pl.GetCellValue(event.GetRow(), 0)
    # self.handle_active_code(st_code, st_name)
```
**What it blocks:** Clicking stocks in the stock pool grid has no effect.

---

### M10. `panel_sim_trade.py:499-527` and `panel_real_trade.py:500-528` — Tree list strategy navigation is mostly stubbed

**Pattern:** Functions that show a message but don't implement real logic
**Code:**
```python
def _ev_click_on_treelist(self, event):
    self.curTreeItem = self.treeListCtrl.GetItemText(event.GetItem())
    if not self.curTreeItem:  # <-- always enters this branch because text is index number
        MessageDialog("当前点击:{0}!".format(self.curTreeItem))  # shows "当前点击:0!"
        # ... tries to match but logic is broken
```
**What it blocks:** The entire strategy navigation tree (策略导航) doesn't work correctly. The condition `if not self.curTreeItem` is always true because `GetItemText` returns the tree node index, not the strategy name. Even if the condition were correct, the data-fetching code is stubbed out.

---

### M11. `panel_sim_trade.py:489-497` and `panel_real_trade.py:490-498` — Trade log dialog has empty OK/Cancel handlers

**Pattern:** Empty handler
**Code:**
```python
def _ev_trade_log(self, event):
    user_trade_log = UserDialog(self, title="回测提示信息", label="交易详细日志")
    if user_trade_log.ShowModal() == wx.ID_OK:
        pass
    else:
        pass
```
**What it blocks:** The trade log dialog opens but does nothing with the result.

---

### M12. `def_dialog.py:737-738` — `_ev_switch_menu` is empty

**Pattern:** Bare pass
**Code:**
```python
def _ev_switch_menu(self, event):
    pass
```
**What it blocks:** Menu switching in the parameter config dialog is non-functional (though the method appears unused).

---

### M13. `def_treelist.py:29-31` — Custom strategies in tree are marked "未定义" (undefined)

**Pattern:** Hardcoded placeholder data
**Code:**
```python
"自定义策略": [
    {"名称": "yx-zl-1", "标识": "综合", "函数": "未定义"},
    {"名称": "yx-zl-2", "标识": "趋势", "函数": "未定义"},
    {"名称": "yx-zl-3", "标识": "波动", "函数": "未定义"},
],
```
**What it blocks:** All three custom strategies shown in the strategy navigation tree are non-functional placeholders.

---

### M14. `panel_results.py:70` — Commented-out final call in `handle_data`

**Pattern:** Commented-out code
**Code:**
```python
# self.pd.show_df()
```
**Impact:** Minor, but suggests the `handle_data` method was never fully tested in its current form.

---

### M15. `panel_sim_trade.py:302,417,419` and `panel_real_trade.py:304,418,420` — `multi_fact_layout()` and `remove_multi_fact_layout()` are called but never defined

**Pattern:** Missing method definitions
**Code:**
```python
# In on_combobox_strategy_changed and _on_combobox_strategy_changed:
if "多因子" in select_strategy:
    self.multi_fact_layout()       # <-- method does NOT exist
else:
    self.remove_multi_fact_layout()  # <-- method does NOT exist
```
**What it blocks:** Selecting any strategy containing "多因子" in the trade panels will crash with `AttributeError`. The `multi_facts_list` attribute is initialized (line 86/88) but never used, and these methods are called but never defined.

---

### M16. `panel_trade.py:23` — Commented-out "我的自选" (watchlist) tab

**Pattern:** Commented-out feature / disabled tab
**Code:**
```python
# self.trade_tabs.AddPage(FocusSymsPanel(self.trade_tabs), "我的自选(预留)")
```
**What it blocks:** The watchlist/favorites tab is explicitly labeled "预留" (reserved) and disabled. `FocusSymsPanel` does not exist as a file in the codebase.

---

### M17. `mainframe.py:39-68` — Menu bar has no toolbar and no keyboard shortcuts

**Pattern:** Missing feature / incomplete menu
**Code:**
```python
def init_menu_bar(self):
    menuBar = wx.MenuBar(style=wx.MB_DOCKABLE)
    self.SetMenuBar(menuBar)
    setting = wx.Menu()
    menuBar.Append(setting, "&设置")
    # ... only 3 menus: 设置, 工具, 帮助
```
**What it blocks:** No toolbar exists at all. The menu bar only has 3 menus with 5 total items. Common features like File→Open, File→Save, File→Exit, Edit→Preferences are missing. No keyboard accelerators are defined. The "设置" menu only has "参数配置" (1 item), "工具" has 3 items, and "帮助" has only "关于" (1 item).

---

### M18. `widget_matplotlib.py:13` — `btn_bkt` button has no event binding

**Pattern:** Button/menu handler that doesn't connect to real functionality
**Code:**
```python
self.btn_bkt = wx.Button(self, label="投资策略回测分析", pos=(100, 10))
# No EVT_BUTTON binding anywhere
```
**What it blocks:** The "投资策略回测分析" button is rendered but does nothing when clicked. No event handler is bound.

---

### M19. `panel_zhiku.py:131-134` — Notebook "运行" button doesn't actually start the server

**Pattern:** Button that doesn't connect to real functionality
**Code:**
```python
def start_notebook(self, event):
    logger.info("start show onlite notebook ...")
    logger.info(self.local_notebook_url)
    self.notebook_page.show_url(self.local_notebook_url)  # just navigates

def start_online_notebook(self):  # <-- NEVER CALLED from button
    os.popen("jupyter notebook --no-browser --port 8800 ./docs/notebook")
    self.iSNotebookActive = True
```
**What it blocks:** The "运行在线Notebook" button only navigates to `localhost:8800` without starting the Jupyter server. The `start_online_notebook()` method that actually starts the server is never invoked. The button should call `start_online_notebook()` first.

---

## LOW Severity — Minor TODOs, code quality, cosmetic issues

### L1. `mainframe.py:95` — Status bar contains WeChat/public account promotion

**Pattern:** 微信 contact
**Code:**
```python
self.SetStatusText("欢迎使用AI智能量化投研平台！请关注公众号: 迈微AI研习社", 0)
```
**Impact:** Status bar permanently shows a public account promotion. This is an advertisement embedded in the UI.

---

### L2. `mainframe.py:83-87` — About dialog shows public account

**Pattern:** 微信 / 联系
**Code:**
```python
def OnAbout(self, event):
    wx.MessageBox(
        "公众号: 迈微AI研习社",
        "关于 Qbot智能量化投研平台",
        wx.OK | wx.ICON_INFORMATION,
    )
```
**Impact:** The About dialog only shows a WeChat public account name — no version info, no license, no links.

---

### L3. `mainframe.py:123` — Inline TODO comment

**Pattern:** TODO
**Code:**
```python
self.boxH.Add(self.tabs, 1, wx.ALL | wx.EXPAND)  # todo propotion==1为何
```
**Impact:** Developer left a question about wxPython sizer proportions.

---

### L4. `mainframe.py:14-17` — Commented-out imports

**Pattern:** Imported but unused (commented out)
**Code:**
```python
# from qbot.gui.panels.panel_userframe import UserFrame
# from qbot.gui.panels.actions import ActionsPanel
# from qbot.gui.panels.page_timeseries import PageTimeSeries
# from qbot.gui.panels.panels import TimeSeriesAnalysis
```
**Impact:** Four panels are disabled via commented imports.

---

### L5. `def_dialog.py:566-606` — Large blocks of commented-out layout code

**Pattern:** Commented-out code
**Code:** ~40 lines of commented-out `firm_mpl` and `back_mpl` configuration in `ParamsConfigDialog.__init__`.
**Impact:** The "行情可视化参数" (firm_mpl) and "回测可视化参数" (back_mpl) config sections are disabled.

---

### L6. `def_dialog.py:140-141` — Bug: `OnOk` reads wrong field for password

**Pattern:** Bug / incomplete implementation
**Code:**
```python
def OnOk(self, event):
    user = self.text_ctrl1.GetValue()
    password = self.text_ctrl1.GetValue()  # <-- should be text_ctrl2
```
**Impact:** In `InputDialogTwoParameters`, the password field value is never read; instead, the username is read twice.

---

### L7. `def_grid.py:71` — Uses deprecated `DataFrame.iteritems()`

**Pattern:** Deprecated API usage
**Code:**
```python
for col, series in df.iteritems():
```
**Impact:** `iteritems()` was deprecated in pandas 1.5 and removed in pandas 2.0. This will raise an error with modern pandas.

---

### L8. `panel_zhiku.py:73` — Hardcoded default research report

**Pattern:** Hardcoded placeholder
**Code:**
```python
self.combo_yanbao.SetValue("【华泰金工】多因子10：因子合成方法实证分析20190104")
```
**Impact:** The default selected research report is hardcoded. If this PDF doesn't exist in the local directory, the viewer will show an error.

---

### L9. `panel_zhiku.py:111` — NotebookPanel URL is hardcoded localhost

**Pattern:** Hardcoded placeholder
**Code:**
```python
self.local_notebook_url = "http://localhost:8800/tree"
```
**Impact:** The Jupyter notebook URL assumes port 8800 and specific path. The `start_notebook` method (line 131) just navigates to the URL without actually starting the server — `start_online_notebook` (line 136) exists but is never called from the button handler.

---

### L10. `panel_sim_trade.py:311-317` and `panel_real_trade.py:312-318` — Unused imports

**Pattern:** Imported but unused
**Code:** Both files import `matplotlib.pyplot`, `numpy`, `wx.grid`, `wx.html2`, `CollegeTreeListCtrl`, `GridTable` — many of which are used but some may be unnecessary (e.g., `np` and `plt` are imported but never used directly in these files).

---

### L11. `panel_zhiku.py:21, 52, 115` — Empty `__del__` methods

**Pattern:** Empty function body
**Code:**
```python
def __del__(self):
    pass
```
**Impact:** Three panels (`QbotHomePanel`, `YanbaoPanel`, `NotebookPanel`) have empty `__del__` methods that serve no purpose.

---

## Appendix: File-by-File Summary

| File | Status | Key Issues |
|------|--------|------------|
| `__init__.py` | Empty | OK |
| `common/PrintLog.py` | Clean | OK |
| `common/SysFile.py` | Minor | `txt2html` has redundant read (line 80 re-reads after line 77) |
| `config.py` | Clean | OK |
| `elements/def_dialog.py` | **Problems** | WeChat paywall (H5), broken password field (L6), empty `_ev_switch_menu` (M12), commented-out layout (L5), orphaned dialog classes (H10, H11) |
| `elements/def_grid.py` | Minor | Deprecated `iteritems()` (L7) |
| `elements/def_treelist.py` | Minor | Hardcoded "未定义" strategies (M13) |
| `global_event.py` | Clean | OK but module-level instance masks class name |
| `gui_utils.py` | Clean | OK |
| `mainframe.py` | **Problems** | Broken monitoring (H1), TODO (H2), commented-out panels (H3), hardcoded IPs (H4), non-functional menu items (H9), missing toolbar/shortcuts (M17), WeChat promo in status bar (L1, L2) |
| `panels/__init__.py` | Empty | OK |
| `panels/panel_backtest.py` | **Problems** | Undefined `self.code_table` (H7), unbound buttons (M1-M5), unused stub (M6), commented-out tabs (M3) |
| `panels/panel_real_trade.py` | **Problems** | WeChat paywall (H6), stubbed tree navigation (M10), empty handlers (M9, M11), hardcoded trade opts (M8), missing multi_fact methods (M15) |
| `panels/panel_results.py` | **Broken** | Imports non-existent module (H8), dead panel (H12) — completely unusable |
| `panels/panel_sim_trade.py` | **Problems** | WeChat paywall (H6), stubbed tree navigation (M10), empty handlers (M9, M11), hardcoded trade opts (M8), missing multi_fact methods (M15) |
| `panels/panel_trade.py` | Minor | Commented-out FocusSymsPanel (M16) |
| `panels/panel_zhiku.py` | Minor | Hardcoded defaults (L8, L9), empty `__del__` (L11), notebook button doesn't start server (M19) |
| `widgets/__init__.py` | Empty | OK |
| `widgets/widget_matplotlib.py` | Minor | Unbound `btn_bkt` button (M18) |
| `widgets/widget_web.py` | Clean | OK |

---

## Recommendations (Priority Order)

1. **Fix `start_monitoring` in `mainframe.py`** — Invert the condition, import `grep_pid` or replace with `psutil`.
2. **Fix `on_menu` in `mainframe.py`** — The created `WebPanel` is never added as a tab; either open URLs in a new frame or add as a notebook page.
3. **Remove or replace WeChat paywall prompts** — Replace with clear documentation on how to configure API keys.
4. **Fix `panel_results.py` import** — Either create the missing `widgets/widgets.py` (with `PandasGrid` class) or update the import path to `widgets.widget_matplotlib.MatplotlibPanel`.
5. **Fix `_ev_enter_stcode` in `panel_backtest.py`** — Remove reference to undefined `self.code_table`.
6. **Define `multi_fact_layout()` and `remove_multi_fact_layout()`** — These methods are called but don't exist in either `panel_sim_trade.py` or `panel_real_trade.py`, causing `AttributeError` when selecting multi-factor strategies.
7. **Fix `InputDialogTwoParameters.OnOk` bug** — Read `text_ctrl2` for password.
8. **Fix deprecated `iteritems()`** — Replace with `items()`.
9. **Connect or remove unbound UI controls** — Trade log button, multi-chart combo, portfolio analysis combo, parameter input change handlers, `btn_bkt` in MatplotlibPanel.
10. **Fix notebook panel** — Call `start_online_notebook()` from the button handler, not just navigate to the URL.
11. **Remove orphaned dialog classes** — `WebDialog` and `InputsDialog` are never used.
12. **Replace hardcoded external URLs** — Make them configurable.
13. **Add missing toolbar and keyboard shortcuts** — The menu bar is sparse with no toolbar; consider adding common shortcuts (Ctrl+O, Ctrl+S, Ctrl+Q).

---

## Deep-Dive: Menu System Inventory

| Menu | Item | Handler | Status |
|------|------|---------|--------|
| **设置** | 参数配置 | `on_params_conf` → opens `ParamsConfigDialog` | **Works** |
| **工具** | 蛋卷估值 | `on_menu` → creates orphaned `WebPanel` | **BROKEN** — panel never shown |
| **工具** | 集思录 | `on_menu` → creates orphaned `WebPanel` | **BROKEN** — panel never shown |
| **工具** | 后台监控 | `start_monitoring` → `grep_pid` not imported, inverted logic | **BROKEN** — NameError + wrong logic |
| **帮助** | 关于 | `OnAbout` → shows WeChat public account | **Works** (minimal) |

**Missing menus:** No File, Edit, View, or Window menus. No keyboard shortcuts or accelerators.

---

## Deep-Dive: Dialog Class Inventory

| Dialog Class | Defined In | Instantiated Anywhere? | Status |
|-------------|-----------|----------------------|--------|
| `MessageDialog` | `def_dialog.py` | Yes (many places) | **Works** |
| `ChoiceDialog` | `def_dialog.py` | Yes (crypto account setup) | **Works** |
| `WebDialog` | `def_dialog.py` | **No** | Dead code |
| `InputsDialog` | `def_dialog.py` | **No** | Dead code |
| `InputDialogTwoParameters` | `def_dialog.py` | Yes (crypto key entry) | **Bug** — password reads wrong field |
| `UserDialog` | `def_dialog.py` | Yes (trade log display) | **Works** (opens read-only log) |
| `ParamsConfigDialog` | `def_dialog.py` | Yes (from mainframe menu) | **Works** |

---

## Deep-Dive: Panel Class Inventory

| Panel Class | Defined In | Used In Active GUI? | Status |
|------------|-----------|--------------------|--------|
| `ZhikuPanel` | `panel_zhiku.py` | Yes (`mainframe.py`) | **Works** |
| `PanelBacktest` | `panel_backtest.py` | Yes (`mainframe.py`) | **Works** (with bugs) |
| `TradePanel` | `panel_trade.py` | Yes (`mainframe.py`) | **Works** |
| `SimTradePanel` | `panel_sim_trade.py` | Yes (via `TradePanel`) | **Partially broken** |
| `RealTradePanel` | `panel_real_trade.py` | Yes (via `TradePanel`) | **Partially broken** |
| `ResultsPanel` | `panel_results.py` | **No** | Dead code, broken import |
| `QbotHomePanel` | `panel_zhiku.py` | Yes (via `ZhikuPanel`) | **Works** (web view) |
| `YanbaoPanel` | `panel_zhiku.py` | Yes (via `ZhikuPanel`) | **Works** (PDF viewer) |
| `NotebookPanel` | `panel_zhiku.py` | Yes (via `ZhikuPanel`) | **Partially broken** |
| `MatplotlibPanel` | `widget_matplotlib.py` | Yes (via `ResultsPanel`) | Orphaned (ResultsPanel dead) |
| `WebPanel` | `widget_web.py` | Yes (many places) | **Works** |

---

## Deep-Dive: Buttons with No Event Bindings

| Button Label | File | Line | Bound? | Impact |
|-------------|------|------|--------|--------|
| "交易日志" | `panel_backtest.py` | 502 | **No** (commented out) | Dead button |
| "投资策略回测分析" | `widget_matplotlib.py` | 13 | **No** | Dead button |
| "多子图显示" dropdown | `panel_backtest.py` | 293 | **No** (commented out) | Dead dropdown |
| "投资组合分析" dropdown | `panel_backtest.py` | 311 | **No** (commented out) | Dead dropdown |
| "运行在线Notebook" | `panel_zhiku.py` | 121 | Yes, but handler doesn't start server | **Broken** |
