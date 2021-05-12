import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import tushare as ts
from datetime import datetime, timedelta
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['Songti SC']
mpl.rcParams['axes.unicode_minus'] = False


token = '164ea8b08e081666dd7547ad322c329f0d9ba0f990f622963d98d49a'
pro = ts.pro_api(token)
index = {'上证综指': '000001.SH',
         '深证成指': '399001.SZ',
         '沪深300': '000300.SH',
         '创业板指': '399006.SZ',
         '上证50': '000016.SH',
         '中证500': '000905.SH',
         '中小板指': '399005.SZ',
         '上证180': '000010.SH'}


# 获取当前交易的股票代码和名称
def get_code():
    df = pro.stock_basic(exchange='', list_status='L')
    codes = df.ts_code.values
    names = df.name.values
    stock = dict(zip(names, codes))
    # 合并指数和个股成一个字典
    stocks = dict(stock, **index)
    return stocks


# 获取行情数据
def get_daily_data(stock, start, end):
    # 如果代码在字典index里，则取的是指数数据
    code = get_code()[stock]
    if code in index.values():
        df = pro.index_daily(ts_code=code, start_date=start, end_date=end)
    # 否则取的是个股数据
    else:
        df = pro.daily(ts_code=code, adj='qfq', start_date=start, end_date=end)
    # 将交易日期设置为索引值
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    # 计算收益率
    df['ret'] = df.close / df.close.shift(1) - 1
    return df


hs = get_daily_data('沪深300', '20180101', '')[['close', 'open', 'high', 'low', 'vol']]
# 最近N1个交易日最高价
hs['up'] = ta.MAX(hs.high, timeperiod=20).shift(1)
# 最近N2个交易日最低价
hs['down'] = ta.MIN(hs.low, timeperiod=10).shift(1)
# 每日真实波动幅度
hs['ATR'] = ta.ATR(hs.high, hs.low, hs.close, timeperiod=20)
hs.tail()


def my_strategy(data):
    x1 = data.close > data.up
    x2 = data.close.shift(1) < data.up.shift(1)
    x = x1 & x2
    y1 = data.close < data.down
    y2 = data.close.shift(1) > data.down.shift(1)
    y = y1 & y2
    data.loc[x, 'signal'] = 'buy'
    data.loc[y, 'signal'] = 'sell'
    buy_date = (data[data.signal == 'buy'].index).strftime('%Y%m%d')
    sell_date = (data[data.signal == 'sell'].index).strftime('%Y%m%d')
    buy_close = data[data.signal == 'buy'].close.round(2).tolist()
    sell_close = data[data.signal == 'sell'].close.round(2).tolist()
    return (buy_date, buy_close, sell_date, sell_close)


def strategy(stock, start, end, N1=20, N2=10):
    df = get_daily_data(stock, start, end)
    # 最近N1个交易日最高价
    df['H_N1'] = ta.MAX(df.high, timeperiod=N1)
    # 最近N2个交易日最低价
    df['L_N2'] = ta.MIN(df.low, timeperiod=N2)
    # 当日收盘价>昨天最近N1个交易日最高点时发出信号设置为1
    buy_index = df[df.close > df['H_N1'].shift(1)].index
    df.loc[buy_index, '收盘信号'] = 1
    # 将当日收盘价<昨天最近N2个交易日的最低点时收盘信号设置为0
    sell_index = df[df.close < df['L_N2'].shift(1)].index
    df.loc[sell_index, '收盘信号'] = 0
    df['当天仓位'] = df['收盘信号'].shift(1)
    df['当天仓位'].fillna(method='ffill', inplace=True)
    d = df[df['当天仓位'] == 1].index[0] - timedelta(days=1)
    df1 = df.loc[d:].copy()
    df1['ret'][0] = 0
    df1['当天仓位'][0] = 0
    # 当仓位为1时，买入持仓，当仓位为0时，空仓，计算资金净值
    df1['策略净值'] = (df1.ret.values * df1['当天仓位'].values + 1.0).cumprod()
    df1['指数净值'] = (df1.ret.values + 1.0).cumprod()
    df1['策略收益率'] = df1['策略净值'] / df1['策略净值'].shift(1) - 1
    df1['指数收益率'] = df1.ret
    total_ret = df1[['策略净值', '指数净值']].iloc[-1] - 1
    annual_ret = pow(1 + total_ret, 250 / len(df1)) - 1
    dd = (df1[['策略净值', '指数净值']].cummax() - df1[['策略净值', '指数净值']]) / df1[['策略净值', '指数净值']].cummax()
    d = dd.max()
    beta = df1[['策略收益率', '指数收益率']].cov().iat[0, 1] / df1['指数收益率'].var()
    alpha = (annual_ret['策略净值'] - annual_ret['指数净值'] * beta)
    exReturn = df1['策略收益率'] - 0.03 / 250
    sharper_atio = np.sqrt(len(exReturn)) * exReturn.mean() / exReturn.std()
    TA1 = round(total_ret['策略净值'] * 100, 2)
    TA2 = round(total_ret['指数净值'] * 100, 2)
    AR1 = round(annual_ret['策略净值'] * 100, 2)
    AR2 = round(annual_ret['指数净值'] * 100, 2)
    MD1 = round(d['策略净值'] * 100, 2)
    MD2 = round(d['指数净值'] * 100, 2)
    S = round(sharper_atio, 2)
    df1[['策略净值', '指数净值']].plot(figsize=(15, 7))
    plt.title('海龟交易策略简单回测', size=15)
    bbox = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    plt.text(df1.index[int(len(df1) / 5)], df1['指数净值'].max() / 1.5, f'累计收益率：\
策略{TA1}%，指数{TA2}%;\n年化收益率：策略{AR1}%，指数{AR2}%；\n最大回撤：  策略{MD1}%，指数{MD2}%;\n\
策略alpha: {round(alpha, 2)}，策略beta：{round(beta, 2)}; \n夏普比率：  {S}', size=13, bbox=bbox)
    plt.xlabel('')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.show()
    # return df1.loc[:,['close','ret','H_N1','L_N2','当天仓位','策略净值','指数净值']]


strategy('上证综指', '20050101', '')

strategy('沪深300', '', '')

strategy('创业板指', '', '')

strategy('沪深300', '20180101', '')

strategy('贵州茅台', '20050101', '', N1=20, N2=10)



# 海龟交易法则可以认为是一个完整的交易系统，具备一个完整的交易系统所应该有的所有成分，包括市场、入市、头寸规模、止损/止盈、退出、买卖策略等：
# 市场：买卖什么？
# 头寸规模：买卖多少？
# 入市：什么时候买卖？
# 止损：什么时候放弃一个亏损的头寸？
# 离市：什么时候退出一个盈利的头寸？
# 策略：如何买卖？
#
# 趋势追踪——唐奇安通道
# 海龟交易法则利用唐奇安通道的突破点作为买卖信号指导交易，简单而言唐奇安通道是由一条上轨线、中线和下线组成，上轨线由N1日内最高价构成，
# 下轨线由N2日内最低价计算，当价格冲破上轨是可能的买入信号，反之，冲破下轨时是可能的卖出信号。
#
# 买卖单位及首次建仓
# 海龟交易系统本质上是一个趋势跟随的系统，但是最值得学习的是资金管理尤其是分批建仓及动态止损的部分。书中提到了N值仓位管理法，
# 其中N值与技术指标平均真实波幅 ATR计算类似。ATR是真实波幅TR的20日平均值，而TR是当前交易日最高价和最低价之差、
# 前一交易日收盘价与当前交易日最高价之差、前一交易日收盘价与当前交易日最低价之差三者中的最大值，用公式表示为：
#
# TR=Max(High−Low,abs(High−PreClose),abs(PreClose−Low))，技术指标库TA-Lib提供了直接计算ATR的函数。
#
# 建仓单位：
#
# Unit=（1%∗账户总资金）/N
# 首次建仓的时候，当捕捉到趋势，即价格突破唐奇安上轨时，买入1个unit。其意义就是，让一个N值的波动与你总资金1%的波动对应，
# 如果买入1unit单位的资产，当天震幅使得总资产的变化不超过1%。
#
# 例如：
# 现在你有1万元资金，1%波动就是100元。假如某股票的N（ATR）值为0.1元，100÷0.1元=1000股。也就是说，
# 你的第一笔仓位应该是在其突破上轨（假设为3元）时立刻买入1000股，耗资3000元。
#
# 动态止损或清仓条件
#
# 当股价跌破10日唐奇安通道下沿，清空头寸结束本次交易。当价格比最后一次买入价格下跌2N时，则卖出全部头寸止损。
# 接上面的例子，最后一次加仓价格为3.2。假如此时N值0.2元。当价格下跌到 3.2 - 2*0.2 = 2.8元时，清仓。
# 持仓成本为 （3+3.1+3.2）*1000/3000 = 3.1元。此时亏损 （3.1-2.8）*3000 = 900元， 对于1万来说 这波亏损9%。
#
# 原始的海龟交易采用唐奇安通道来追踪趋势，在趋势比较明显的行情表现不错，但是在震荡的行情中效果不佳，当然这是所有趋势型策略的通病。
# 下面着重使用Python对唐奇安通道进行可视化，并利用简化版的海龟交易法则进行简单的历史回测。