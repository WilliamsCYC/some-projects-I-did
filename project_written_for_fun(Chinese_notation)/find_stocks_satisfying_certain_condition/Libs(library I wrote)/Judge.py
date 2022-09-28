import numpy as np
from sklearn.linear_model import LinearRegression


# 启明星部分
# 普通版
def judge_qi_a(close, openP, body2):
    body_len_of_qi = 0.02                # 启明星第二天实体的涨幅
    range_of_decline_qi = 0.03           # 启明星第一天跌幅的最小值
    chong_die_qi = 0.005                 # 启明星第二天与其余两天允许的重叠范围
    a = np.array([(close[-3]-openP[-3])/openP[-3]<-range_of_decline_qi,
                  close[-3]>max(close[-2],openP[-2])*(1+chong_die_qi),
                  body2/openP[-2] <= body_len_of_qi,
                  close[-1]>openP[-1],
                  openP[-1]>max(close[-2],openP[-2])*(1+chong_die_qi),
                  close[-1]>(openP[-3]+abs(openP[-3]-close[-3])*0.6)                   # 第三天的涨幅超过第一天实体的60%
                ])
    if a.all() == 1:
        return True


# 加入十字星
def judge_qi_b(close, openP, body2):
    body_len_of_qi = 0.005  # 启明星第二天实体的涨幅(要求是十字星)
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


# 第三天的涨幅完全覆盖第一天
def judge_qi_c(close, openP, body2):
    body_len_of_qi = 0.02                # 启明星第二天实体的涨幅
    range_of_decline_qi = 0.03           # 启明星第一天跌幅的最小值
    chong_die_qi = 0.005                 # 启明星第二天与其余两天允许的重叠范围
    a = np.array([(close[-3]-openP[-3])/openP[-3]<-range_of_decline_qi,
                  close[-3]>max(close[-2],openP[-2])*(1+chong_die_qi),
                  body2/openP[-2] <= body_len_of_qi,
                  close[-1]>openP[-1],
                  openP[-1]>max(close[-2],openP[-2])*(1+chong_die_qi),
                  close[-1]>openP[-3]                                       # 第三天覆盖第一天
                ])
    if a.all() == 1:
        return True


# 第二天成交量减小，第三天成交量放大
def judge_qi_d(close, openP, body2, turn, turn_MA10):
    body_len_of_qi = 0.02                # 启明星第二天实体的涨幅
    range_of_decline_qi = 0.03           # 启明星第一天跌幅的最小值
    chong_die_qi = 0.005                 # 启明星第二天与其余两天允许的重叠范围
    a = np.array([(close[-3]-openP[-3])/openP[-3]<-range_of_decline_qi,
                  close[-3]>max(close[-2],openP[-2])*(1+chong_die_qi),
                  body2/openP[-2] <= body_len_of_qi,
                  close[-1]>openP[-1],
                  openP[-1]>max(close[-2],openP[-2])*(1+chong_die_qi),
                  close[-1]>(openP[-3]+abs(openP[-3]-close[-3])*0.6),                   # 第三天的涨幅超过第一天实体的60%
                  turn[-2]<turn_MA10[-2]*0.8,
                  turn[-1]>turn_MA10[-1]*1.2
                ])
    if a.all() == 1:
        return True











# 孕平锤部分
# 判断前第i天是不是孕线
def judge_yun(i, openP, close):
    body_len_of_yun_1 = 0.035  # 孕线第一天实体的最小跌幅
    a = np.array([(close[-(i + 1)] - openP[-(i + 1)]) / close[-(i + 1)] <= -body_len_of_yun_1,
                  max(openP[-i], close[-i]) < openP[-(i + 1)],
                  min(openP[-i], close[-i]) > close[-(i + 1)],
                  ])
    if a.all() == 1:
        return True


# 判断前第i天与前第(i+1)天是否组成平头底部
def judge_ping_tou(i, low, close):
    dif_of_low = 0.01  # 平头底形态两日最低价的差所占股价的变化幅度
    if abs(low[-i] - low[-(i + 1)]) < close[-i] * dif_of_low:
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
    if a.all() == 1:
        return True









# 锤子部分
# 判断快速下跌
# 逻辑：第i天之前的j天的收盘价线性回归系数小于-1.0    j默认是6天
def judge_kuai_su_xia_die(i, j, close):
    X = []
    for d in range(j):
        X.append(d + 1)
    X = np.array(X).reshape(-1, 1)
    Y = []
    for d in range(j):
        Y.append(close[-(i + j - d)])
    Y = np.array(Y).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, Y)
    k = model.coef_
    if k[0][0] <= -1:
        return True

    # 判断前第i天是不是锤子线


def judge_chui_a(i, bodyi, down_shadow_i, up_shadow_i, openP):
    down_shadow_of_hammer = 2  # 锤子线下影线对实体部分的比例
    up_shadow_of_hammer = 0.5  # 锤子线上影线对实体部分的比例
    body_len_of_hammer = 0.02  # 锤子线实体的涨幅
    a = np.array([bodyi / openP[-i] <= body_len_of_hammer,
                  down_shadow_i / bodyi >= down_shadow_of_hammer,
                  up_shadow_i / bodyi <= up_shadow_of_hammer
                  ])
    return a


# 判断急速下跌后出现的锤子线：要求之前快速下跌，出现一根锤子线,且锤子线的最低价要是近期低点，然后下一天收盘价高于锤子线实体（这个是用来打分的）
def judge_chui_zi(i, bodyi, down_shadow_i, up_shadow_i, openP, close, low, j=6):
    # 快速下跌
    if judge_kuai_su_xia_die(i, j, close):
        # 前第二天是锤子线
        chui_zi_xian_2 = judge_chui_a(i, bodyi, down_shadow_i, up_shadow_i, openP)
        di_dian = np.array([low[-2] < min(low[-3], low[-4], low[-5], low[-6], low[-7], low[-8])])
        if chui_zi_xian_2.all() == 1 and di_dian.all() == 1:
            # 下一天收盘价高于锤子线实体
            if close[-1] > max(openP[-2], close[-2]):
                return True










# 孕十字部分
# 判断前第i天是不是孕线
def judge_yun(i, openP, close):
    body_len_of_yun_1 = 0.035  # 孕线第一天实体的最小跌幅
    body_len_of_yun_2 = 0.02  # 孕线第二天实体的最大涨幅
    a = np.array([(close[-(i + 1)] - openP[-(i + 1)]) / close[-(i + 1)] <= -body_len_of_yun_1,
                  max(openP[-i], close[-i]) < openP[-(i + 1)],
                  min(openP[-i], close[-i]) > close[-(i + 1)],
                  ])
    if a.all() == 1:
        return True


# 判断前第i天是不是长脚十字
def judge_shi_zi(i, bodyi, down_shadow_i, openP):
    a = np.array([bodyi / openP[-i] < 0.01,
                  down_shadow_i / openP[-1] > 0.03,
                  ])
    if a.all() == 1:
        return True