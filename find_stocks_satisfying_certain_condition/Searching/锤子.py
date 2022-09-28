from Data_Process import *
from Open_Data import *


whole_list, data = Open_data()

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


def judge_chui(i, bodyi, down_shadow_i, up_shadow_i, openP):
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
        chui_zi_xian_2 = judge_chui(i, bodyi, down_shadow_i, up_shadow_i, openP)
        di_dian = np.array([low[-2] < min(low[-3], low[-4], low[-5], low[-6], low[-7], low[-8])])
        if chui_zi_xian_2.all() == 1 and di_dian.all() == 1:
            # 下一天收盘价高于锤子线实体
            if close[-1] > max(openP[-2], close[-2]):
                return True

buylist = []

for sec in whole_list:
    d_sec = data[data['ts_code'] == sec]
    d_sec = d_sec.set_index('trade_date').sort_index()
    if len(d_sec) < 25:
        continue

    close, openP, high, low, turn, body1, body2, body3, up_shadow_1, up_shadow_2, up_shadow_3, down_shadow_1, down_shadow_2, down_shadow_3, Pct_change_1, Pct_change_2, MA5, MA10, MA15, turn_MA10 = Get_all_Data(d_sec)


    if judge_xia_die(MA5, MA10, MA15):
        if judge_chui_zi(2, body2, down_shadow_2, up_shadow_2, openP, close, low, j=6):
            buylist.append(sec)

print(buylist)