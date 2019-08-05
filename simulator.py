import tushare as ts

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from calculation import calculate_profit_for_single_stock, grid_search_single_stock

import warnings
warnings.filterwarnings("ignore")

#设置好需要用到的参数
#向前看的天数（设置开始日期为多少天之前）
days_count = [365, 730]
#股票代码
stock_code = '000001.SZ'
#市场类型
market_type = 'stock'
#移动平均天数
MA_dates = [7,14]
#使用多长时间的K线图
#K_dates = 1
#使用何种K线图，可以选择‘daily’/‘weekly’/‘monthly’
K_type = ['daily']
#每笔交易费用
transaction_fee_rate = 0.0008
#滑点费用
slippage_fee_rate = 0.002
#利息费用
interest_fee_rate = 0.001
#利息的种类，可以选择按天的D，按月的M
interest_type = 'D'
#杠杆费用
leverage_fee_rate = 0.001
#初始资金
start_money = 10000

#读取tushare的token
pro = ts.pro_api('6f92d455dd39756f84ddb2c7a785c346e6c3bfa7cafd9bcaedf9b4e9')

# now = datetime.datetime.now()
# delta = datetime.timedelta(days=days_count)
#
# n_days = now - delta
# start_date = n_days.strftime('%Y%m%d')
# print (start_date)

if __name__ == '__main__':
    print(grid_search_single_stock(start_money, days_count, stock_code, MA_dates, K_type, transaction_fee_rate, show_process=False))
