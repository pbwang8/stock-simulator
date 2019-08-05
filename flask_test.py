from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from calculation import grid_search_single_stock

app = Flask(__name__)
bootstrap = Bootstrap(app)


html = '''
    <!DOCTYPE html>
    <title>Simulator</title>
    <h1>拟态-MA 策略</h1>
    <form method=post enctype=multipart/form-data>
        Stock Code: <br>
        <input type="text" name="stock_code" size="20" value="000001.SZ">
        <br><br>
        Back Days: Seperated by comma<br>
        <input type="text" name="days_count" size="20" value="365,730">
        <br><br>
        Market Type: ("support stock only for now") <br>
        <input type="text" name="market_type" size="20" value="stock">
        <br><br>
        MA Dates: Seperated by comma<br>
        <input type="text" name="MA_dates" size="20" value="7,14">
        <br><br>
        K Line Type: Seperated by comma ("daily or weekly") <br>
        <input type="text" name="K_type" size="20" value="daily">
        <br><br>
        Transaction Fee Rate: <br>
        <input type="text" name="transaction_fee_rate" size="20" value="0.0008">
        <br><br>
        Start Money: <br>
        <input type="text" name="start_money" size="20" value="10000">
        <br><br>
        <input type=submit value="Calculate">
    </form>
    '''

@app.route('/', methods = ['GET','POST'])
def single_stock_calculation():
    if request.method == 'POST':
        print(request.form)
        days_count = list(map(int, request.form['days_count'].split(",")))
        stock_code = request.form['stock_code']
        market_type = request.form['market_type']
        MA_dates = list(map(int, request.form['MA_dates'].split(",")))
        K_type = request.form['K_type'].split(",")
        transaction_fee_rate = float(request.form['transaction_fee_rate'])
        start_money = int(request.form['start_money'])
        result = grid_search_single_stock(start_money, days_count, stock_code, MA_dates, K_type, transaction_fee_rate, show_process=False)
        print(result)
        return render_template('simple.html',  tables=[result.to_html(classes='data', header="true")])
    else:
        return html

@app.route('/calculation_result')
def calculation_result():
    return "NA for now"

if __name__ == '__main__':
   app.run(debug = True)



#设置好需要用到的参数
#向前看的天数（设置开始日期为多少天之前）
days_count = 365
#股票代码
stock_code = '000001.SZ'
#市场类型
market_type = 'stock'
#移动平均天数
MA_dates = 7
#使用多长时间的K线图
#K_dates = 1
#使用何种K线图，可以选择‘daily’/‘weekly’/‘monthly’
K_type = 'daily'
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
