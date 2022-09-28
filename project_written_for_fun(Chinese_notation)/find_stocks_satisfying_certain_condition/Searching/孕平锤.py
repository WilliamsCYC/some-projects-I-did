from Data_Process import *
from Open_Data import *


whole_list, data = Open_data()

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


buylist = []

for sec in whole_list:
    d_sec = data[data['ts_code'] == sec]
    d_sec = d_sec.set_index('trade_date').sort_index()
    if len(d_sec) < 25:
        continue

    close, openP, high, low, turn, body1, body2, body3, up_shadow_1, up_shadow_2, up_shadow_3, down_shadow_1, down_shadow_2, down_shadow_3, Pct_change_1, Pct_change_2, MA5, MA10, MA15, turn_MA10 = Get_all_Data(d_sec)

    if judge_xia_die(MA5, MA10, MA15):
        if judge_yun(1, openP, close) and judge_ping_tou(1, low, close) and judge_chui(1, body1, down_shadow_1,up_shadow_1, openP):
            buylist.append(sec)

print(buylist)