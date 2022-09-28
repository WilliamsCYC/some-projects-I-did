import talib as ta
import numpy as np


# 获得前第i天的实体（价格变动的绝对值）
def get_body(i, openP, close):
    a = abs(openP[-i]-close[-i])
    if a == 0:
        a = 0.0001
    return a


# 获得前第i天的涨跌幅（包含正负号，不是绝对值）
def get_Pct_change(i, openP, close):
    a = (close[-1]-openP[-1])/openP[-1]
    return a


# 获得前第i天的上影线
def get_up_shadow(i, high, openP, close):
    a = high[-i]-max(openP[-i], close[-i])
    return a


# 获得前第i天的下影线
def get_down_shadow(i, low, openP, close):
    a = min(openP[-i], close[-i])-low[-i]
    return a


# 判断下跌
def judge_xia_die(MA5, MA10, MA15):
    # 5，10，15排列
    a = np.array([MA5[-3]<MA10[-3]<MA15[-3], MA5[-4]<MA10[-4]<MA15[-4], MA5[-5]<MA10[-5]<MA15[-5], MA5[-6]<MA10[-6]<MA15[-6], MA5[-7]<MA10[-7]<MA15[-7]])
    # 五日均线和十日均线
    # xia_die = np.array([MA5[-5] < MA10[-5], MA5[-6] < MA10[-6], MA5[-7] < MA10[-7], MA5[-8] < MA10[-8], MA10[-5] < MA20[-5], MA10[-6] < MA20[-6], MA10[-7] < MA20[-7], MA10[-8] < MA20[-8], MA10[-9] < MA20[-9]])
    # 十日均线和二十日均线
    # xia_die = np.array([MA10[-1] < MA20[-1], MA10[-2] < MA20[-2], MA10[-3] < MA20[-3], MA10[-4] < MA20[-4], MA10[-5] < MA20[-5]])
    if a.all() == 1:
        return True


# 输出所有基本指标
def Get_all_Data(d_sec):
    close = np.array(d_sec['close'])
    openP = np.array(d_sec['open'])
    high = np.array(d_sec['high'])
    low = np.array(d_sec['low'])
    turn = np.array(d_sec['vol'])

    body1 = get_body(1, openP, close)
    body2 = get_body(2, openP, close)
    body3 = get_body(3, openP, close)
    up_shadow_1 = get_up_shadow(1, high, openP, close)
    down_shadow_1 = get_down_shadow(1, low, openP, close)
    up_shadow_2 = get_up_shadow(2, high, openP, close)
    down_shadow_2 = get_down_shadow(2, low, openP, close)
    up_shadow_3 = get_up_shadow(3, high, openP, close)
    down_shadow_3 = get_down_shadow(3, low, openP, close)
    Pct_change_1 = get_Pct_change(1, openP, close)
    Pct_change_2 = get_Pct_change(2, openP, close)

    MA5 = ta.MA(close, 5)
    MA10 = ta.MA(close, 10)
    MA15 = ta.MA(close, 15)

    turn_MA10 = ta.MA(turn, 10)

    return close, openP, high, low, turn, body1, body2, body3, up_shadow_1, up_shadow_2, up_shadow_3, down_shadow_1, down_shadow_2, down_shadow_3, Pct_change_1, Pct_change_2, MA5, MA10, MA15, turn_MA10