"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-05-20 16:37:34
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-09-20 10:16:19
FilePath: /Qbot/gui/panels/panel_backtest.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
"""
import wx

from qbot.common.file_utils import extract_content
from qbot.common.logging.logger import LOGGER as logger
from qbot.common.macros import strategy_choices
from qbot.gui import gui_utils
from qbot.gui.config import DATA_DIR_BKT_RESULT
from qbot.gui.elements.def_dialog import MessageDialog
from qbot.gui.widgets.widget_web import WebPanel

import re
from datetime import datetime
import importlib

import akshare as ak
import backtrader as bt
import numpy as np
import pandas as pd
import yfinance as yf
from pyecharts.charts import Kline, Line
from pyecharts import options as opts


# Strategy registry: map display name → (module_path, class_name)
STRATEGY_REGISTRY = {
    "单因子-相对强弱指数RSI": ("qbot.strategies.rsi_strategy_bt", "RSIStrategy"),
    "单因子-简单移动均线": ("qbot.strategies.sma_cross_strategy_bt", "SmaCross"),
    "单因子-布林线均值回归": ("qbot.strategies.boll_strategy_bt", "BollStrategy"),
    "机器学习-麻雀优化算法SSA": ("qbot.strategies.ssa_strategy_bt", "MyStrategy"),
    "多因子-ROC(20)动量信号周频Top1": ("qbot.strategies.multi_strategy_bt", "MultiStrategy"),
}


# https://zhuanlan.zhihu.com/p/376248349
def OnBkt(event):
    wx.MessageBox("ok")


class PanelBacktest(wx.Panel):
    def __init__(self, parent=None, id=-1, displaySize=(1600, 900)):
        super(PanelBacktest, self).__init__(parent)

        self.backtest_opts = {
            "start_time": "20100101",
            "end_time": "20211231",
            "benchmark": "000300.SH",
            "code": "399006.SZ",
            "select_strategy": "单因子-相对强弱指数RSI",
        }

        self.backtest_config = {
            "limit_threshold": 0.095,
            "init_cash": 10000,
            "deal_price": "close",
            "open_cost": 0.0005,
            "slippage": 0.1,
            "stake": 100,  # 每笔交易量
            "commission": 0.0005,
            "stamp_duty": 0.001,
            "close_cost": 0.0015,
            "min_cost": 5,
        }

        # M1 与 M2 横向布局时宽度分割
        self.M1_width = int(displaySize[0] * 0.1)
        self.M2_width = int(displaySize[0] * 0.9)
        # M1 纵向100%
        self.M1_length = int(displaySize[1])

        # M1中S1 S2 S3 纵向布局高度分割
        self.M1S1_length = int(self.M1_length * 0.2)
        self.M1S2_length = int(self.M1_length * 0.2)
        self.M1S3_length = int(self.M1_length * 0.6)

        self.BackWebPanel = WebPanel(self)

        # 第二层布局
        self.vbox_sizer_b = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        self.vbox_sizer_b.Add(
            self._init_para_notebook(),
            proportion=1,
            flag=wx.EXPAND | wx.BOTTOM,
            border=5,
        )  # 添加行情参数布局
        # self.vbox_sizer_b.Add(
        #     self.patten_log_tx, proportion=10, flag=wx.EXPAND | wx.BOTTOM, border=5
        # )

        self.vbox_sizer_b.Add(
            self.BackWebPanel,
            proportion=10,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )

        # 第一层布局
        self.HBoxPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.HBoxPanelSizer.Add(
            self.vbox_sizer_b, proportion=0, border=2, flag=wx.EXPAND | wx.ALL
        )
        self.SetSizer(self.HBoxPanelSizer)  # 使布局有效

        # self.layout()

    def layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox)

        hbox.Add(wx.StaticText(self, label="请选择基准:"))
        combo_benchmarks = wx.ComboBox(self, size=(190, 25), pos=(10, 120))
        combo_benchmarks.SetItems(["沪深300指数(000300.SH)", "标普500指数(SPY)"])
        hbox.Add(combo_benchmarks)

        # vbox.Add(panel, 0)
        btn = wx.Button(self, label="开始回测", style=1)
        self.Bind(wx.EVT_BUTTON, self.StartBacktest, btn)
        vbox.Add(btn)

        # 底部是一个浏览器
        web = WebPanel(self)
        vbox.Add(web, 1, wx.EXPAND)
        web.show_file(DATA_DIR_BKT_RESULT.joinpath("bkt_result.html"))

        # web.show_url('http://www.jisilu.cn')

        self.web = web

    def _init_para_notebook(self):

        # 创建参数区面板
        self.ParaNoteb = wx.Notebook(self)
        self.ParaStPanel = wx.Panel(self.ParaNoteb, -1)  # 行情
        self.ParaBtPanel = wx.Panel(self.ParaNoteb, -1)  # 回测 back test
        self.ParaPtPanel = wx.Panel(self.ParaNoteb, -1)  # 条件选股 pick stock
        self.ParaPaPanel = wx.Panel(self.ParaNoteb, -1)  # 形态选股 patten

        # 第二层布局
        self.ParaStPanel.SetSizer(self.add_stock_para_lay(self.ParaStPanel))
        self.ParaBtPanel.SetSizer(self.add_backt_para_lay(self.ParaBtPanel))
        # self.ParaPtPanel.SetSizer(self.add_pick_para_lay(self.ParaPtPanel))
        # self.ParaPaPanel.SetSizer(self.add_patten_para_lay(self.ParaPaPanel))

        self.ParaNoteb.AddPage(self.ParaStPanel, "行情参数")
        self.ParaNoteb.AddPage(self.ParaBtPanel, "回测参数")
        # self.ParaNoteb.AddPage(self.ParaPtPanel, "条件选股")
        # self.ParaNoteb.AddPage(self.ParaPaPanel, "形态选股")

        return self.ParaNoteb

    def add_stock_para_lay(self, sub_panel):

        # 行情参数
        stock_para_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 行情参数——日历控件时间周期
        self.dpc_end_time = wx.adv.DatePickerCtrl(
            sub_panel,
            -1,
            style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE,
        )  # 结束时间
        self.dpc_start_time = wx.adv.DatePickerCtrl(
            sub_panel,
            -1,
            style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE,
        )  # 起始时间

        self.start_date_box = wx.StaticBox(sub_panel, -1, "开始日期(Start)")
        self.end_date_box = wx.StaticBox(sub_panel, -1, "结束日期(End)")
        self.start_date_sizer = wx.StaticBoxSizer(self.start_date_box, wx.VERTICAL)
        self.end_date_sizer = wx.StaticBoxSizer(self.end_date_box, wx.VERTICAL)
        self.start_date_sizer.Add(
            self.dpc_start_time,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        self.end_date_sizer.Add(
            self.dpc_end_time,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        date_time_now = wx.DateTime.Now()  # wx.DateTime格式"03/03/18 00:00:00"
        self.dpc_end_time.SetValue(date_time_now)
        self.dpc_start_time.SetValue(date_time_now.SetYear(date_time_now.year - 1))

        self.Bind(wx.adv.EVT_DATE_CHANGED, self._on_end_time_changed, self.dpc_end_time)
        self.Bind(
            wx.adv.EVT_DATE_CHANGED, self._on_start_time_changed, self.dpc_start_time
        )

        self.backtest_opts["end_time"] = gui_utils._wxdate2pydate(
            self.dpc_end_time.GetValue()
        ).strftime("%Y%m%d")
        self.backtest_opts["start_time"] = gui_utils._wxdate2pydate(
            self.dpc_start_time.GetValue()
        ).strftime("%Y%m%d")

        # 行情参数——输入股票代码
        self.stock_code_box = wx.StaticBox(sub_panel, -1, "交易标的(股票/期货/比特币)代码")
        self.stock_code_sizer = wx.StaticBoxSizer(self.stock_code_box, wx.VERTICAL)
        self.stock_code_input = wx.TextCtrl(
            sub_panel, -1, "399006.SZ", style=wx.TE_PROCESS_ENTER
        )
        self.stock_code_sizer.Add(
            self.stock_code_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        self.stock_code_input.Bind(wx.EVT_TEXT_ENTER, self._ev_enter_stcode)
        self.Bind(wx.EVT_TEXT, self._on_combobox_code_changed, self.stock_code_input)
        select_code = self.stock_code_input.GetValue()
        logger.debug(f"select_code: {select_code}")
        self.backtest_opts["code"] = select_code

        # 行情参数——股票周期选择
        self.stock_period_box = wx.StaticBox(sub_panel, -1, "股票周期")
        self.stock_period_sizer = wx.StaticBoxSizer(self.stock_period_box, wx.VERTICAL)
        self.stock_period_cbox = wx.ComboBox(
            sub_panel, -1, "", choices=["30分钟", "60分钟", "日线", "周线"]
        )
        self.stock_period_cbox.SetSelection(2)
        self.stock_period_sizer.Add(
            self.stock_period_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 行情参数——股票复权选择
        self.stock_authority_box = wx.StaticBox(sub_panel, -1, "股票复权")
        self.stock_authority_sizer = wx.StaticBoxSizer(
            self.stock_authority_box, wx.VERTICAL
        )
        self.stock_authority_cbox = wx.ComboBox(
            sub_panel, -1, "", choices=["前复权", "后复权", "不复权"]
        )
        self.stock_authority_cbox.SetSelection(2)
        self.stock_authority_sizer.Add(
            self.stock_authority_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 行情参数——多子图显示
        self.pick_graph_box = wx.StaticBox(sub_panel, -1, "多子图显示")
        self.pick_graph_sizer = wx.StaticBoxSizer(self.pick_graph_box, wx.VERTICAL)
        self.pick_graph_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "未开启",
            choices=[
                "未开启",
                "A股票走势-MPL",
                "B股票走势-MPL",
                "C股票走势-MPL",
                "D股票走势-MPL",
                "A股票走势-WEB",
                "B股票走势-WEB",
                "C股票走势-WEB",
                "D股票走势-WEB",
            ],
            style=wx.CB_READONLY | wx.CB_DROPDOWN,
        )
        self.pick_graph_cbox.SetSelection(0)
        self.pick_graph_last = self.pick_graph_cbox.GetSelection()
        self.pick_graph_sizer.Add(
            self.pick_graph_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        # self.pick_graph_cbox.Bind(wx.EVT_COMBOBOX, self._ev_select_graph)

        # 行情参数——股票组合分析
        self.group_analy_box = wx.StaticBox(sub_panel, -1, "投资组合分析")
        self.group_analy_sizer = wx.StaticBoxSizer(self.group_analy_box, wx.VERTICAL)
        self.group_analy_cmbo = wx.ComboBox(
            sub_panel,
            -1,
            "预留A",
            choices=["预留A", "收益率/波动率", "走势叠加分析", "财务指标评分-预留"],
            style=wx.CB_READONLY | wx.CB_DROPDOWN,
        )  # 策略名称
        self.group_analy_sizer.Add(
            self.group_analy_cmbo,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        # self.group_analy_cmbo.Bind(wx.EVT_COMBOBOX, self._ev_group_analy)  # 绑定ComboBox事件

        # 回测按钮
        self.load_data_but = wx.Button(sub_panel, -1, "加载行情数据")
        self.load_data_but.SetBackgroundColour(wx.Colour(76, 187, 23))  # 设置背景颜色
        # self.load_data_but.Bind(wx.EVT_BUTTON, self._ev_start_run)  # 绑定按钮事件
        self.load_data_but.Bind(wx.EVT_BUTTON, self.LoadData)  # 绑定按钮事件

        stock_para_sizer.Add(
            self.start_date_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.CENTER | wx.ALL,
            border=5,
        )
        stock_para_sizer.Add(
            self.end_date_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        stock_para_sizer.Add(
            self.stock_code_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        stock_para_sizer.Add(
            self.stock_period_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        stock_para_sizer.Add(
            self.stock_authority_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        stock_para_sizer.Add(
            self.pick_graph_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        stock_para_sizer.Add(
            self.group_analy_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        stock_para_sizer.Add(
            self.load_data_but,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )

        return stock_para_sizer

    def add_backt_para_lay(self, sub_panel):

        # 回测参数
        back_para_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 行情参数——输入股票基准
        self.stock_benchmark_box = wx.StaticBox(sub_panel, -1, "回测基准选取")
        self.stock_benchmark_sizer = wx.StaticBoxSizer(
            self.stock_benchmark_box, wx.VERTICAL
        )
        self.stock_benchmark_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=["沪深300指数(000300.SH)", "标普500指数(SPX)", "恒生指数(HSI)"],
        )
        self.stock_benchmark_cbox.SetSelection(0)
        self.stock_benchmark_cbox.Bind(wx.EVT_COMBOBOX, self._on_combobox_benchmarks_changed)  # noqa: E501
        self.select_benchmark = self.stock_benchmark_cbox.GetValue()
        self.benchmark_code = extract_content(self.select_benchmark)[0]
        logger.debug(f"select_benchmark: {self.benchmark_code}")
        self.backtest_opts["benchmark"] = self.benchmark_code
        self.stock_benchmark_sizer.Add(
            self.stock_benchmark_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 行情参数——初始资金
        self.init_cash_box = wx.StaticBox(sub_panel, -1, "初始资金")
        self.init_cash_sizer = wx.StaticBoxSizer(self.init_cash_box, wx.VERTICAL)
        self.init_cash_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["init_cash"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_init_cash_changed, self.init_cash_input)
        self.init_cash_sizer.Add(
            self.init_cash_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_stake_box = wx.StaticBox(sub_panel, -1, "交易规模")
        self.init_stake_sizer = wx.StaticBoxSizer(self.init_stake_box, wx.VERTICAL)
        self.init_stake_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["stake"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_stake_changed, self.init_stake_input)
        self.init_stake_sizer.Add(
            self.init_stake_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_slippage_box = wx.StaticBox(sub_panel, -1, "滑点")
        self.init_slippage_sizer = wx.StaticBoxSizer(
            self.init_slippage_box, wx.VERTICAL
        )
        self.init_slippage_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["slippage"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_slippage_changed, self.init_slippage_input)
        self.init_slippage_sizer.Add(
            self.init_slippage_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_commission_box = wx.StaticBox(sub_panel, -1, "手续费")
        self.init_commission_sizer = wx.StaticBoxSizer(
            self.init_commission_box, wx.VERTICAL
        )
        self.init_commission_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["commission"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_commission_changed, self.init_commission_input)
        self.init_commission_sizer.Add(
            self.init_commission_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_tax_box = wx.StaticBox(sub_panel, -1, "印花税")
        self.init_tax_sizer = wx.StaticBoxSizer(self.init_tax_box, wx.VERTICAL)
        self.init_tax_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["stamp_duty"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_stamp_duty_changed, self.init_tax_input)
        self.init_tax_sizer.Add(
            self.init_tax_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 行情参数——回测策略选择
        self.stock_strategy_box = wx.StaticBox(sub_panel, -1, "回测策略选取")
        self.stock_strategy_sizer = wx.StaticBoxSizer(
            self.stock_strategy_box, wx.HORIZONTAL
        )
        self.stock_strategy_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=list(strategy_choices)[0],
            style=wx.CB_READONLY | wx.CB_DROPDOWN,
        )
        self.stock_strategy_cbox.SetSelection(0)
        self.stock_strategy_sizer.Add(
            self.stock_strategy_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        # self.stock_strategy_cbox.Bind(wx.EVT_RADIOBUTTON, self._ev_src_choose)
        self.stock_strategy_cbox.Bind(wx.EVT_COMBOBOX, self._on_combobox_strategy_changed)
        select_strategy = self.stock_strategy_cbox.GetStringSelection()
        self.backtest_opts["select_strategy"] = select_strategy
        logger.debug(f"select_strategy: {select_strategy}")

        # 回测按钮
        self.start_back_but = wx.Button(sub_panel, -1, "开始回测")
        self.start_back_but.SetBackgroundColour(wx.Colour(76, 187, 23))  # 设置背景颜色
        # self.start_back_but.Bind(wx.EVT_BUTTON, self._ev_start_run)  # 绑定按钮事件
        self.start_back_but.Bind(wx.EVT_BUTTON, self.StartBacktest)  # 绑定按钮事件

        # 交易日志
        self.trade_log_but = wx.Button(sub_panel, -1, "交易日志")
        # self.trade_log_but.Bind(wx.EVT_BUTTON, self._ev_trade_log)  # 绑定按钮事件

        self.BackWebPanel.show_file(DATA_DIR_BKT_RESULT.joinpath("bkt_result.html"))

        back_para_sizer.Add(
            self.stock_benchmark_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_cash_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_stake_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_slippage_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_commission_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_tax_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.stock_strategy_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.start_back_but,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.trade_log_but,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )

        return back_para_sizer

    def _ev_enter_stcode(self, event):  # 输入股票代码

        # 第一步:收集控件中设置的选项
        st_code = self.stock_code_input.GetValue()
        st_name = self.code_table.get_name(st_code)
        self.backtest_opts["code"] = st_code
        logger.info(f"回测股票/基金: You select {st_code}")

    def _on_start_time_changed(self, event):
        start_time = gui_utils._wxdate2pydate(self.dpc_start_time.GetValue()).strftime(
            "%Y%m%d"
        )
        self.backtest_opts["start_time"] = start_time
        logger.info(f"start_time: {start_time}")

    def _on_end_time_changed(self, event):
        end_time = gui_utils._wxdate2pydate(self.dpc_end_time.GetValue()).strftime(
            "%Y%m%d"
        )
        self.backtest_opts["end_time"] = end_time
        logger.info(f"end_time: {end_time}")

    def _on_init_cash_changed(self, event):
        self.backtest_config["init_cash"] = self.init_cash_input.GetValue()

    def _on_slippage_changed(self, event):
        self.backtest_config["slippage"] = self.init_slippage_input.GetValue()

    def _on_stake_changed(self, event):
        self.backtest_config["stake"] = self.init_stake_input.GetValue()

    def _on_commission_changed(self, event):
        self.backtest_config["commission"] = self.init_commission_input.GetValue()

    def _on_stamp_duty_changed(self, event):
        self.backtest_config["stamp_duty"] = self.init_tax_input.GetValue()

    # def _on_text_changed(self, event):
    #     with open(RESULT_DIR.joinpath("backtest.log"), "r") as f:
    #         self.log_text_ctrl.SetValue(f.read())

    def _on_combobox_benchmarks_changed(self, event):
        self.select_benchmark = self.stock_benchmark_cbox.GetValue()
        self.benchmark_code = extract_content(self.select_benchmark)[0]
        logger.debug(f"select_benchmark: {self.benchmark_code}")
        self.backtest_opts["benchmark"] = self.benchmark_code
        logger.info(f"基准: You select {self.benchmark_code}")

        # data_files_tmp = [x for x in self.data_files if x != self.benchmark_code]
        # # logger.debug(f"new code list: {data_files_tmp}")
        # self.combo_codes.SetItems(data_files_tmp)
        # self.combo_codes.SetValue("399006.SZ")

    def _on_combobox_strategy_changed(self, event):
        select_strategy = self.stock_strategy_cbox.GetValue()
        self.backtest_opts["select_strategy"] = select_strategy
        logger.info(f"交易策略: You select {select_strategy}")

    def _on_combobox_code_changed(self, event):
        select_code = self.stock_code_input.GetValue()
        self.backtest_opts["code"] = select_code
        logger.info(f"回测股票/基金: You select {select_code}")

    def _ev_trade_log(self, event):
        pass

    def StartBacktest(self, event):
        """Run backtrader backtest with selected strategy and loaded data."""
        # 1. Check data loaded
        if not hasattr(self, 'stock_dat') or self.stock_dat is None or self.stock_dat.empty:
            MessageDialog("请先加载行情数据")
            return

        # 2. Get params from UI
        strategy_name = self.backtest_opts.get("select_strategy", "")
        code = self.backtest_opts.get("code", "unknown")
        try:
            init_cash = float(self.init_cash_input.GetValue())
            stake = int(self.init_stake_input.GetValue())
            commission = float(self.init_commission_input.GetValue())
            slippage_val = float(self.init_slippage_input.GetValue())
            stamp_duty = float(self.init_tax_input.GetValue())
        except ValueError as e:
            MessageDialog(f"回测参数错误: {e}")
            return

        # 3. Resolve strategy class
        if strategy_name not in STRATEGY_REGISTRY:
            MessageDialog(f"该策略尚未实现: {strategy_name}")
            return

        module_path, class_name = STRATEGY_REGISTRY[strategy_name]
        try:
            mod = importlib.import_module(module_path)
            strategy_class = getattr(mod, class_name)
        except (ImportError, AttributeError) as e:
            MessageDialog(f"加载策略失败: {e}")
            return

        try:
            # 4. Prepare data for backtrader
            df = self.stock_dat.copy()
            df.index = pd.to_datetime(df["Date"])
            if hasattr(df.index, 'tz') and df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            df_bt = df[["Open", "High", "Low", "Close", "Volume"]].copy()
            df_bt.columns = [c.lower() for c in df_bt.columns]
            df_bt["openinterest"] = 0

            start_date = df.index.min().to_pydatetime()
            end_date = df.index.max().to_pydatetime()

            data = bt.feeds.PandasData(
                dataname=df_bt,
                fromdate=start_date,
                todate=end_date,
            )

            # 5. Setup Cerebro
            cerebro = bt.Cerebro(stdstats=True)
            cerebro.adddata(data)
            cerebro.addstrategy(strategy_class)
            cerebro.broker.setcash(init_cash)
            # Combined commission (trading fee + stamp duty)
            cerebro.broker.setcommission(commission=commission + stamp_duty)
            # Use percentage sizer: invest 95% of available cash per trade
            # This avoids the "can't afford 100 shares" problem
            cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
            if slippage_val > 0:
                cerebro.broker.set_slippage_perc(perc=slippage_val / 100)

            # Add observers for equity curve tracking
            cerebro.addobserver(bt.observers.Value)

            # Add analyzers
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.04)
            cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
            cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='timereturn')

            # 6. Run backtest
            logger.info(f"Starting backtest: {code}, strategy={strategy_name}, cash={init_cash}")
            results = cerebro.run()
            strat = results[0]
            final_value = cerebro.broker.getvalue()
            pnl = final_value - init_cash
            pnl_pct = (pnl / init_cash) * 100

            # Extract analyzers
            sharpe_result = strat.analyzers.sharpe.get_analysis()
            sharpe_ratio = sharpe_result.get('sharperatio', None)
            if sharpe_ratio is None:
                sharpe_ratio = sharpe_result.get('sharpe_ratio', 'N/A')

            # Trade stats
            trade_analysis = strat.analyzers.trades.get_analysis()
            total_trades = trade_analysis.get('total', {}).get('total', 0)
            won = trade_analysis.get('won', {}).get('total', 0)
            lost = trade_analysis.get('lost', {}).get('total', 0)

            # Warn if no trades
            if total_trades == 0:
                MessageDialog(
                    f"回测完成但无交易产生\n\n"
                    f"策略 {strategy_name} 在该时间段内未触发买卖信号。\n"
                    f"可能原因：\n"
                    f"1. 数据日期范围太短\n"
                    f"2. 股票趋势太强，未出现超买/超卖\n\n"
                    f"建议：扩大日期范围或换一只波动更大的股票"
                )
                return

            # 7. Build equity curve from TimeReturn analyzer
            time_returns = strat.analyzers.timereturn.get_analysis()
            dates = df.index.tolist()
            equity_curve = [init_cash]
            for i, dt_key in enumerate(sorted(time_returns.keys())):
                if i < len(dates) - 1:
                    equity_curve.append(equity_curve[-1] * (1 + time_returns[dt_key]))
            # Pad if needed
            while len(equity_curve) < len(dates):
                equity_curve.append(equity_curve[-1])
            equity_curve = equity_curve[:len(dates)]

            date_labels = [d.strftime('%Y-%m-%d') for d in dates]

            # Build benchmark curve from user-selected index
            benchmark_code = self.backtest_opts.get("benchmark", "000300.SH")
            benchmark_name_map = {
                "000300.SH": "沪深300", "SPX": "标普500", "HSI": "恒生指数"
            }
            benchmark_label = f"基准({benchmark_name_map.get(benchmark_code, benchmark_code)})"

            start_dt_str = start_date.strftime("%Y%m%d")
            end_dt_str = end_date.strftime("%Y%m%d")
            index_closes = self._fetch_benchmark_index(
                benchmark_code, start_dt_str, end_dt_str
            )

            if index_closes and len(index_closes) > 0:
                first_index_close = float(index_closes[0])
                if first_index_close == 0:
                    first_index_close = 1.0
                benchmark_curve = []
                for i in range(len(dates)):
                    if i < len(index_closes):
                        bm_val = init_cash * float(index_closes[i]) / first_index_close
                    else:
                        bm_val = init_cash * float(index_closes[-1]) / first_index_close
                    benchmark_curve.append(round(bm_val, 2))
                logger.info(
                    f"Benchmark curve from {benchmark_code}, "
                    f"{len(index_closes)} points"
                )
            else:
                # Fallback: stock buy-and-hold
                benchmark_label = "基准(Buy&Hold — 指数数据获取失败)"
                benchmark_curve = []
                first_close = float(df.iloc[0]["Close"])
                for i in range(len(dates)):
                    bm_val = init_cash * float(df.iloc[i]["Close"]) / first_close
                    benchmark_curve.append(round(bm_val, 2))
                logger.warning(
                    f"Benchmark {benchmark_code} fetch failed, "
                    f"using stock B&H fallback"
                )

            # Create pyecharts line chart
            line = Line()
            line.add_xaxis(date_labels)
            line.add_yaxis(
                "策略净值",
                [round(v, 2) for v in equity_curve],
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2),
                label_opts=opts.LabelOpts(is_show=False),
                areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            )
            line.add_yaxis(
                benchmark_label,
                benchmark_curve,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2),
                label_opts=opts.LabelOpts(is_show=False),
            )
            line.set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{code} 回测结果 — {strategy_name}",
                    subtitle=(
                        f"初始: {init_cash:,.0f} → 期末: {final_value:,.2f} | "
                        f"收益: {pnl:+,.2f} ({pnl_pct:+.2f}%) | "
                        f"交易: {total_trades}次 (胜{won}/负{lost}) | Sharpe: {sharpe_ratio}"
                    ),
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axislabel_opts=opts.LabelOpts(rotate=45),
                ),
                yaxis_opts=opts.AxisOpts(type_="value"),
                datazoom_opts=[
                    opts.DataZoomOpts(range_start=0, range_end=100),
                    opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
                ],
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                legend_opts=opts.LegendOpts(),
            )

            html_path = DATA_DIR_BKT_RESULT.joinpath(f"{code}_backtest_result.html")
            line.render(str(html_path))
            logger.info(f"Backtest result saved to {html_path}")

            # 8. Display in WebPanel
            self.BackWebPanel.show_file(str(html_path))

            # 9. Show summary dialog
            sharpe_str = f"{sharpe_ratio:.4f}" if isinstance(sharpe_ratio, (int, float)) else str(sharpe_ratio)
            summary = (
                f"回测完成\n\n"
                f"策略: {strategy_name}\n"
                f"标的: {code}\n"
                f"初始资金: {init_cash:,.0f}\n"
                f"期末资金: {final_value:,.2f}\n"
                f"收益: {pnl:+,.2f} ({pnl_pct:+.2f}%)\n"
                f"交易次数: {total_trades} (胜{won}/负{lost})\n"
                f"Sharpe Ratio: {sharpe_str}"
            )
            MessageDialog(summary)
            logger.info(f"Backtest done: PnL={pnl:+,.2f} ({pnl_pct:+.2f}%), trades={total_trades}")

        except Exception as e:
            logger.error(f"StartBacktest error: {e}")
            import traceback
            traceback.print_exc()
            MessageDialog(f"回测出错: {str(e)}")

    def _is_chinese_stock(self, code):
        code_upper = code.upper()
        if code_upper.endswith(".SZ") or code_upper.endswith(".SH"):
            return True
        if re.match(r"^\d{6}$", code_upper):
            return True
        return False

    def _is_hk_stock(self, code):
        code_upper = code.upper()
        if code_upper.endswith(".HK"):
            return True
        if re.match(r"^\d{4,5}$", code):
            # 4-5 digit pure numbers likely HK stocks (e.g. 02513, 9992)
            return True
        return False

    def _strip_stock_suffix(self, code):
        code_upper = code.upper()
        for suffix in (".SZ", ".SH", ".HK"):
            if code_upper.endswith(suffix):
                return code_upper[:-3]
        return code_upper

    def _map_period(self, period_str):
        mapping = {"30分钟": "30", "60分钟": "60", "日线": "daily", "周线": "weekly"}
        return mapping.get(period_str, "daily")

    def _map_adjust(self, adjust_str):
        mapping = {"前复权": "qfq", "后复权": "hfq", "不复权": ""}
        return mapping.get(adjust_str, "")

    def _fetch_with_retry(self, fetch_fn, max_retries=3, delay=2):
        """Retry wrapper for unstable API calls."""
        import time
        last_err = None
        for attempt in range(max_retries):
            try:
                df = fetch_fn()
                if df is not None and not df.empty:
                    return df
            except Exception as e:
                last_err = e
                logger.warning(f"Fetch attempt {attempt+1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
        if last_err:
            raise last_err
        return None

    def _fetch_cn_stock(self, code, start_time, end_time):
        symbol = self._strip_stock_suffix(code)
        period = self._map_period(self.stock_period_cbox.GetValue())
        adjust = self._map_adjust(self.stock_authority_cbox.GetValue())
        logger.info(
            f"Fetching CN stock: {symbol}, period={period}, "
            f"start={start_time}, end={end_time}, adjust={adjust}"
        )
        def _do_fetch():
            return ak.stock_zh_a_hist(
                symbol=symbol, period=period,
                start_date=start_time, end_date=end_time,
                adjust=adjust,
            )
        df = self._fetch_with_retry(_do_fetch)
        if df is None or df.empty:
            return None
        df.rename(
            columns={
                "日期": "Date", "开盘": "Open", "收盘": "Close",
                "最高": "High", "最低": "Low", "成交量": "Volume",
            },
            inplace=True,
        )
        df["Date"] = pd.to_datetime(df["Date"])
        for col in ["Open", "High", "Low", "Close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def _fetch_hk_stock(self, code, start_time, end_time):
        symbol = self._strip_stock_suffix(code)
        # akshare HK stock uses 5-digit string e.g. "02513"
        if len(symbol) < 5:
            symbol = symbol.zfill(5)
        period = self._map_period(self.stock_period_cbox.GetValue())
        adjust = self._map_adjust(self.stock_authority_cbox.GetValue())
        logger.info(
            f"Fetching HK stock: {symbol}, period={period}, "
            f"start={start_time}, end={end_time}, adjust={adjust}"
        )
        def _do_fetch():
            return ak.stock_hk_hist(
                symbol=symbol, period=period,
                start_date=start_time, end_date=end_time,
                adjust=adjust,
            )
        df = self._fetch_with_retry(_do_fetch)
        if df is None or df.empty:
            # Fallback: try yfinance with .HK suffix
            logger.info(f"akshare HK failed, trying yfinance for {symbol}.HK")
            ticker = yf.Ticker(f"{symbol}.HK")
            start_dt = datetime.strptime(start_time, "%Y%m%d")
            end_dt = datetime.strptime(end_time, "%Y%m%d")
            df = ticker.history(start=start_dt.strftime("%Y-%m-%d"), end=end_dt.strftime("%Y-%m-%d"))
            if df is None or df.empty:
                return None
            df.reset_index(inplace=True)
            keep_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
            df = df[[c for c in keep_cols if c in df.columns]]
            if "Date" in df.columns and hasattr(df["Date"], "dt"):
                df["Date"] = df["Date"].dt.tz_localize(None)
            df.sort_values("Date", inplace=True)
            df.reset_index(drop=True, inplace=True)
            return df
        df.rename(
            columns={
                "日期": "Date", "开盘": "Open", "收盘": "Close",
                "最高": "High", "最低": "Low", "成交量": "Volume",
            },
            inplace=True,
        )
        df["Date"] = pd.to_datetime(df["Date"])
        for col in ["Open", "High", "Low", "Close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def _fetch_us_stock(self, code, start_time, end_time):
        start_dt = datetime.strptime(start_time, "%Y%m%d")
        end_dt = datetime.strptime(end_time, "%Y%m%d")
        start_str = start_dt.strftime("%Y-%m-%d")
        end_str = end_dt.strftime("%Y-%m-%d")
        logger.info(
            f"Fetching US stock: {code}, start={start_str}, end={end_str}"
        )
        ticker = yf.Ticker(code)
        df = ticker.history(start=start_str, end=end_str)
        if df is None or df.empty:
            return None
        df.reset_index(inplace=True)
        keep_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
        df = df[[c for c in keep_cols if c in df.columns]]
        if "Date" in df.columns and hasattr(df["Date"], "dt"):
            df["Date"] = df["Date"].dt.tz_localize(None)
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def _fetch_benchmark_index(self, benchmark_code, start_time, end_time):
        """Fetch benchmark index close prices for the given date range.
        Returns list of close prices, or None on failure."""
        try:
            if benchmark_code == "000300.SH":
                df = ak.stock_zh_index_daily(symbol="sh000300")
                if df is None or df.empty:
                    return None
                date_col = "date" if "date" in df.columns else df.columns[0]
                df[date_col] = pd.to_datetime(df[date_col])
                start_dt = datetime.strptime(start_time, "%Y%m%d")
                end_dt = datetime.strptime(end_time, "%Y%m%d")
                mask = (df[date_col] >= start_dt) & (df[date_col] <= end_dt)
                df = df[mask].sort_values(date_col)
                # Find close column (akshare uses lowercase)
                close_col = None
                for c in df.columns:
                    if str(c).lower() == "close":
                        close_col = c
                        break
                if close_col is None:
                    return None
                return df[close_col].tolist()

            elif benchmark_code in ("SPX", "HSI"):
                ticker_map = {"SPX": "^GSPC", "HSI": "^HSI"}
                ticker = ticker_map[benchmark_code]
                start_dt = datetime.strptime(start_time, "%Y%m%d")
                end_dt = datetime.strptime(end_time, "%Y%m%d")
                df = yf.download(
                    ticker,
                    start=start_dt.strftime("%Y-%m-%d"),
                    end=end_dt.strftime("%Y-%m-%d"),
                    progress=False,
                )
                if df is None or df.empty:
                    return None
                # yfinance may return MultiIndex columns
                if isinstance(df.columns, pd.MultiIndex):
                    close_cols = [c for c in df.columns if c[0] == "Close"]
                    close_col = close_cols[0] if close_cols else None
                elif "Close" in df.columns:
                    close_col = "Close"
                else:
                    close_col = None
                if close_col is None:
                    return None
                return df[close_col].tolist()

            return None
        except Exception as e:
            logger.warning(f"Failed to fetch benchmark {benchmark_code}: {e}")
            return None

    def _generate_kline_html(self, df, code):
        dates = df["Date"].dt.strftime("%Y-%m-%d").tolist()
        kline_data = []
        for _, row in df.iterrows():
            kline_data.append([
                float(row["Open"]),
                float(row["Close"]),
                float(row["Low"]),
                float(row["High"]),
            ])

        kline = Kline()
        kline.add_xaxis(dates)
        kline.add_yaxis(code, kline_data)
        kline.set_global_opts(
            title_opts=opts.TitleOpts(title=f"{code} K线图"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(rotate=45),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=50, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=50, range_end=100),
            ],
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
        )
        html_path = DATA_DIR_BKT_RESULT.joinpath(f"{code}_kline.html")
        kline.render(str(html_path))
        logger.info(f"K-line chart saved to {html_path}")
        return html_path

    def LoadData(self, event):
        code = self.backtest_opts.get("code", "").strip()
        start_time = self.backtest_opts.get("start_time", "")
        end_time = self.backtest_opts.get("end_time", "")

        if not code:
            MessageDialog("请输入股票代码")
            return

        try:
            if self._is_chinese_stock(code):
                df = self._fetch_cn_stock(code, start_time, end_time)
            elif self._is_hk_stock(code):
                df = self._fetch_hk_stock(code, start_time, end_time)
            else:
                df = self._fetch_us_stock(code, start_time, end_time)

            if df is None or df.empty:
                MessageDialog(f"获取数据失败，请检查股票代码: {code}")
                return

            self.stock_dat = df

            html_path = self._generate_kline_html(df, code)
            self.BackWebPanel.show_file(str(html_path))

            logger.info(f"成功加载 {code} 行情数据，共 {len(df)} 条记录")

        except Exception as e:
            logger.error(f"LoadData error: {e}")
            MessageDialog(f"加载数据出错: {str(e)}")
