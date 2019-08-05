import tushare as ts

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import warnings
warnings.filterwarnings("ignore")

pro = ts.pro_api('6f92d455dd39756f84ddb2c7a785c346e6c3bfa7cafd9bcaedf9b4e9')

def pltStockMA(rev_stock, MA_dates, K_type, stock_code):
    plt.figure()
    plt.figure(figsize=(20,8))
    xs = [datetime.datetime.strptime(d, '%Y%m%d').date() for d in rev_stock['trade_date']]
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(bymonthday=1))
    plt.plot(xs, rev_stock['close'], label = 'close')
    plt.plot(xs, rev_stock['MA'], label = 'MA')
    plt.axis()
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.title("K-line-%s and MA-%s on %s"%(K_type, MA_dates, stock_code))
    plt.xlabel("Dates")
    plt.ylabel("price")
    plt.legend(loc = 'lower right')
    plt.grid()
    plt.show()
    return()

#计算回测收益的函数
#规则为在时间窗口内的第一次收盘价的值大于MA值之后的第二天开盘价买入，然后在接下来的每次收盘价的值小于MA值之后的第二天开盘价卖出
#暂时没考虑做空
def lookback_profit(start_money, rev_stock, transaction_fee_rate, show_process=False):
    position_status = 0
    position_shares = 0
    total_transaction_time = 0
    total_buyin_time = 0
    total_sell_time = 0
    transaction_share = 0
    transaction_fee_total = 0
    available_money = start_money
    for i in range(len(rev_stock)-1):
        if (position_status == 0) and (rev_stock['close'][i] > rev_stock['MA'][i]):
            position_status = 1
            transaction_price = rev_stock['open'][i+1]
            transaction_share = available_money/transaction_price
            #手续费为手续费（暂时没有加上滑点费用）
            transaction_fee = transaction_price * transaction_share * transaction_fee_rate
            transaction_fee_total += transaction_fee
            available_money = 0
            total_asset = available_money + transaction_price*transaction_share - transaction_fee
            total_transaction_time += 1
            total_buyin_time += 1
            if (show_process == True):
                print('Breakdown Time: %d '%total_transaction_time)
                print('Buyin Time: %d'%total_buyin_time)
                print('Breakdown Date: %s '%rev_stock['trade_date'][i])
                print('Transaction Date: %s '%rev_stock['trade_date'][i+1])
                print('Transaction Type: %d '%position_status)
                print('Transaction Price: %f '%transaction_price)
                print('Transaction Share: %f '%transaction_share)
                print('Total Asset: %f\n '%total_asset)
        if (position_status == 1) and (rev_stock['close'][i] < rev_stock['MA'][i]):
            position_status = 0
            transaction_price = rev_stock['open'][i+1]
            #transaction_share = transaction_share
            transaction_fee = transaction_price * transaction_share * transaction_fee_rate
            transaction_fee_total += transaction_fee
            available_money += transaction_price * transaction_share - transaction_fee
            total_asset = available_money
            total_transaction_time += 1
            total_sell_time += 1
            if (show_process == True):
                print('Breakdown Time: %d '%total_transaction_time)
                print('Sell Time: %d'%total_sell_time)
                print('Breakdown Date: %s '%rev_stock['trade_date'][i])
                print('Transaction Date: %s '%rev_stock['trade_date'][i+1])
                print('Transaction Type: %d '%position_status)
                print('Transaction Price: %f '%transaction_price)
                print('Transaction Share: %f '%transaction_share)
                print('Total Asset: %f\n '%total_asset)
    final_asset = total_asset
    final_profit = final_asset - start_money
    final_profit_rate = final_profit / start_money
    print ('Final profit rate: %f'%final_profit_rate)
    print ('Total transaction fee: %f'%transaction_fee_total)
    return (final_profit_rate)

def calculate_profit_for_single_stock(start_money, days_count, stock_code, MA_dates, K_type, transaction_fee_rate, show_process=False):
    #得到开始日期
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days_count)
    n_days = now - delta
    start_date = n_days.strftime('%Y%m%d')

    #得到时间对应的股票价格走势表格
    single_stock = pro.query(K_type, ts_code=stock_code, start_date=start_date, fields = 'ts_code, trade_date, open, high, low, close')
    rev_stock = single_stock.iloc[::-1].reset_index(drop = True)
    rev_stock['MA'] = rev_stock['close'].rolling(window=MA_dates).mean()

    #pltStockMA(rev_stock, MA_dates, K_type, stock_code)

    start_price = list(rev_stock['open'])[0]
    end_price = list(rev_stock['open'])[-1]
    profit_original = (end_price-start_price)/start_price
    print ('Original profit rate: %f'%profit_original)

    profit_rate = lookback_profit(start_money, rev_stock, transaction_fee_rate, show_process)
    return(profit_rate, profit_original)

def calculate_annual_profit(days, profit):
    start_value = 1
    after_value = 1+profit
    daily_profit = after_value ** (1/days)
    annual_profit = daily_profit ** 365 - 1
    return(annual_profit)

def grid_search_single_stock(start_money, Time_periods, stock_code, MA_dates_list, K_type_list, transaction_fee_rate, show_process=False):
    return_df = pd.DataFrame()
    stock_code_list = []
    profit_rate_list = []
    k_type_list = []
    ma_dates_list = []
    time_periods_list = []
    profit_annual_list = []
    profit_original_list = []
    profit_original_annual_list = []
    profit_annual_win_list = []
    for k in K_type_list:
        for j in Time_periods:
            for i in MA_dates_list:
                stock_code_list.append(stock_code)
                k_type_list.append(k)
                ma_dates_list.append(i)
                time_periods_list.append(j)
                profit_rate, profit_original = calculate_profit_for_single_stock(start_money, j, stock_code, i, k, transaction_fee_rate, show_process)
                profit_rate_list.append(profit_rate)
                profit_original_list.append(profit_original)
                profit_annual = calculate_annual_profit(j, profit_rate)
                profit_annual_list.append(profit_annual)
                profit_original_annual = calculate_annual_profit(j, profit_original)
                profit_original_annual_list.append(profit_original_annual)
                profit_annual_win_list.append(profit_annual-profit_original_annual)
    return_df['stock_code'] = stock_code_list
    return_df['K_type'] = k_type_list
    return_df['MA_dates'] = ma_dates_list
    return_df['Time_periods'] = time_periods_list
    return_df['Profit_rate'] = profit_rate_list
    return_df['Profit_rate_annual'] = profit_annual_list
    return_df['Profit_original'] = profit_original_list
    return_df['Profit_original_annual'] = profit_original_annual_list
    return_df['Profit_annual_win'] = profit_annual_win_list
    return (return_df)
