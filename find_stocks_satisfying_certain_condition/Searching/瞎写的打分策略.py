from Data_Process import *
from Open_Data import *


whole_list, data = Open_data()

# 判断快速下跌
# 逻辑：第i天之前的j天的收盘价线性回归系数小于-1.0    j默认是6天
def judge_kuai_su_xia_die(i, j, close):
    X = []
    for d in range(j):
        X.append(d+1)
    X = np.array(X).reshape(-1,1)
    Y = []
    for d in range(j):
        Y.append(close[-(i+j-d)])
    Y = np.array(Y).reshape(-1,1)
    model = LinearRegression()
    model.fit(X,Y)
    k = model.coef_
    if k[0][0] <= -1:
        return True

# 判断急速下跌后出现的锤子线：要求之前快速下跌，出现一根锤子线,且锤子线的最低价要是近期低点，然后下一天收盘价高于锤子线实体（这个是用来打分的）
def judge_chui_zi(i, bodyi, down_shadow_i, up_shadow_i, openP, close, low, j=6):
    # 快速下跌
    if judge_kuai_su_xia_die(i, j, close):
        # 前第二天是锤子线
        chui_zi_xian_2 = judge_chui(i, bodyi, down_shadow_i, up_shadow_i, openP)
        di_dian = np.array([low[-2] < min(low[-3], low[-4], low[-5], low[-6], low[-7], low[-8])])
        if chui_zi_xian_2.all() == 1 and di_dian.all() == 1:
            # 下一天收盘价高于锤子线实体
            if close[-1] > max(openP[-2], close[-2]):
                return True


# 判断前第i天是不是锤子线
def judge_chui(i, bodyi, down_shadow_i, up_shadow_i, openP):
    down_shadow_of_hammer = 2  # 锤子线下影线对实体部分的比例
    up_shadow_of_hammer = 0.5  # 锤子线上影线对实体部分的比例
    body_len_of_hammer = 0.02  # 锤子线实体的涨幅
    a = np.array([bodyi / openP[-i] <= body_len_of_hammer,
                  down_shadow_i / bodyi >= down_shadow_of_hammer,
                  up_shadow_i / bodyi <= up_shadow_of_hammer
                  ])
    return a


# 判断前第i天与前第(i+1)天是否组成平头底部
def judge_ping_tou(i, low, close):
    dif_of_low = 0.006  # 平头底形态两日最低价的差所占股价的变化幅度
    if abs(low[-i] - low[-(i + 1)]) < close[-i] * dif_of_low:
        return True


# 判断前第i天与前第(i+1)天是否组成看涨吞没，第二天的实体涨幅要超过4%
def judge_tun(i, close, openP, Pct_change_1, Pct_change_2):
    # 看涨吞没应该分成两种情况讨论

    # 第一种：（普通）第一天的下跌幅度超过2%
    range_of_open_tun = 0.006  # 看涨吞没第二天开盘价允许超过第一天收盘价的范围
    a = np.array([close[-i] > openP[-i],
                  close[-(i + 1)] < openP[-(i + 1)],
                  close[-i] > openP[-(i + 1)],
                  openP[-i] < close[-(i + 1)] * (1 + range_of_open_tun),
                  Pct_change_1 > 0.04,
                  Pct_change_2 < -0.02
                  ])

    # 第二种：（加分）第一天的下跌幅度在0.1%到2%以内，即不能是十字星
    b = np.array([close[-i] > openP[-i],
                  close[-(i + 1)] < openP[-(i + 1)],
                  close[-i] > openP[-(i + 1)],
                  openP[-1] < close[-(i + 1)],
                  Pct_change_1 > 0.04,
                  -0.02 < Pct_change_2 < -0.001
                  ])

    # 第三种：（再加分）第一天是十字星，此时不要求第一天是下跌
    c = np.array([close[-i] > openP[-i],
                  close[-i] > openP[-(i + 1)],
                  openP[-1] < close[-(i + 1)],
                  Pct_change_1 > 0.04,
                  Pct_change_2 > 0.02,
                  -0.001 < Pct_change_2 < 0.001
                  ])

    if c.all() == 1:
        return 3
    elif b.all() == 1:
        return 2
    elif a.all() == 1:
        return 1
    else:
        return 0

    # 判断前第i天与前第(i+1)天是否组成刺透形态


def judge_ci_tou(i, close, openP, bodyi):
    a = np.array([close[-i] > openP[-i],
                  close[-(i + 1)] < openP[-(i + 1)],
                  openP[-i] < close[-(i + 1)],
                  close[-i] > (close[-(i + 1)] + bodyi * 0.5)
                  ])
    if a.all() == 1:
        return True


# 判断前第i天是不是孕线
def judge_yun(i, Pct_change_i, openP, close):
    body_len_of_yun_1 = 0.06  # 孕线第一天实体的最小跌幅
    body_len_of_yun_2 = 0.02  # 孕线第二天实体的最大涨幅
    a = np.array([(close[-(i + 1)] - openP[-(i + 1)]) / close[-(i + 1)] <= -body_len_of_yun_1,
                  max(openP[-i], close[-i]) < openP[-(i + 1)],
                  min(openP[-i], close[-i]) > close[-(i + 1)],
                  abs(Pct_change_i) < body_len_of_yun_2
                  ])
    if a.all() == 1:
        return True


# 判断启明星
def judge_qi(close, openP, body2):
    body_len_of_qi = 0.02  # 启明星第二天实体的涨幅
    range_of_decline_qi = 0.03  # 启明星第一天跌幅的最小值
    chong_die_qi = 0.005  # 启明星第二天与其余两天允许的重叠范围
    a = np.array([(close[-3] - openP[-3]) / openP[-3] < -range_of_decline_qi,
                  close[-3] > max(close[-2], openP[-2]) * (1 + chong_die_qi),
                  body2 / openP[-2] <= body_len_of_qi,
                  close[-1] > openP[-1],
                  openP[-1] > max(close[-2], openP[-2]) * (1 + chong_die_qi),
                  close[-1] > (openP[-3] + abs(openP[-3] - close[-3]) * 0.6)  # 第三天的涨幅超过第一天实体的60%
                  ])
    if a.all() == 1:
        return True


# 判断前三天当中是否有向上跳空
def judge_tiao_kong(low, high):
    tiao_kong_1 = np.array([low[-1] > high[-2]])
    tiao_kong_2 = np.array([low[-2] > high[-3]])
    tiao_kong = np.array([tiao_kong_1.all(), tiao_kong_2.all()])
    if tiao_kong.any() == 1:
        return True


# 判断多个技术指标的结合形态
def he_ti(a=np.array([1]), b=np.array([1]), c=np.array([1]), m=True, n=True):
    x = np.array([a, b.all(), c.all(), m, n])
    if x.all() == 1:
        return True


multiple_vol_tun = 2  # 看涨吞没形态第二天的交易量超过十日成交量均线的倍数，用来加分

buylist = []

for sec in whole_list:
    d_sec = data[data['ts_code'] == sec]
    d_sec = d_sec.set_index('trade_date').sort_index()
    if len(d_sec) < 25:
        continue

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

    # 打分
    # 判断处于下跌过程
    fen = 0
    if judge_xia_die(MA5, MA10, MA15):

        # 判断锤子线
        chui_zi_xian_1 = judge_chui(1, body1, down_shadow_1, up_shadow_1, openP)
        chui_zi_xian_2 = judge_chui(2, body2, down_shadow_2, up_shadow_2, openP)
        chui_zi_xian_3 = judge_chui(3, body3, down_shadow_3, up_shadow_3, openP)

        # 判断平头底中夹带锤子线
        if he_ti(judge_ping_tou(1, low, close), chui_zi_xian_1.all(), chui_zi_xian_2.all()) or he_ti(
                judge_ping_tou(2, low, close), chui_zi_xian_2.all(), chui_zi_xian_3.all()):
            fen += 0.6
            a = 1
            b = 0
        # 判断平头底
        elif judge_ping_tou(1, low, close) or judge_ping_tou(2, low, close):
            fen += 0.4
            b = 1
            a = 0
        else:
            a = 0
            b = 0

        # 判断孕线中夹带锤子线
        if he_ti(judge_yun(1, Pct_change_1, openP, close), chui_zi_xian_1, chui_zi_xian_2) or he_ti(
                judge_yun(2, Pct_change_2, openP, close), chui_zi_xian_2, chui_zi_xian_3):
            fen += 0.5
            c = 1
            d = 0
        # 判断孕线
        elif judge_yun(1, Pct_change_1, openP, close) or judge_yun(2, Pct_change_2, openP, close):
            fen += 0.3
            d = 1
            c = 0
        else:
            c = 0
            d = 0

        # 判断快速下跌后出现锤子线
        if judge_chui_zi(2, body2, down_shadow_2, up_shadow_2, openP, close, low, j=6):
            fen += 1.0

            # 判断看涨吞没以及第二天放量
        if he_ti(judge_tun(1, close, openP, Pct_change_1, Pct_change_2) > 0,
                 b=np.array([turn[-1] > turn_MA10[-1] * multiple_vol_tun])):
            fen += 0.6
            e = 1
            f = 0
            g = 0
        # 判断看涨吞没
        elif judge_tun(1, close, openP, Pct_change_1, Pct_change_2) == 3:
            fen += 0.6
            e = 0
            f = 1
            g = 0
        elif judge_tun(1, close, openP, Pct_change_1, Pct_change_2) == 2:
            fen += 0.5
            e = 0
            f = 1
            g = 0
        elif judge_tun(1, close, openP, Pct_change_1, Pct_change_2) == 1:
            fen += 0.4
            e = 0
            f = 1
            g = 0
        # 判断刺透形态
        elif judge_ci_tou(1, close, openP, body2) or judge_ci_tou(2, close, openP, body3):
            fen += 0.3
            e = 0
            f = 0
            g = 1
        else:
            e = 0
            f = 0
            g = 0

        # 判断启明星
        if judge_qi(close, openP, body2):
            fen += 0.6
            h = 1
        else:
            h = 0

        # 判断跳空
        if judge_tiao_kong(low, high):
            fen += 0.4
            i = 1
        else:
            i = 0

    if fen >= 1.0:
        buylist.append(sec)
        print('a=', a, 'b=', b, 'c=', c, 'd=', d, 'e=', e, 'f=', f, 'g=', g, 'h=', h, 'i=', i)

print(buylist)