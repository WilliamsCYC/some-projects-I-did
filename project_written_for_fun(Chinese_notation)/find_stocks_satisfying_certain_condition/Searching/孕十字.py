from Data_Process import *
from Open_Data import *


whole_list, data = Open_data()

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

buylist = []

for sec in whole_list:
    d_sec = data[data['ts_code'] == sec]
    d_sec = d_sec.set_index('trade_date').sort_index()
    if len(d_sec) < 25:
        continue

    close, openP, high, low, turn, body1, body2, body3, up_shadow_1, up_shadow_2, up_shadow_3, down_shadow_1, down_shadow_2, down_shadow_3, Pct_change_1, Pct_change_2, MA5, MA10, MA15, turn_MA10 = Get_all_Data(d_sec)

    if judge_xia_die(MA5, MA10, MA15):
        if judge_yun(1, openP, close) and judge_shi_zi(1, body1, down_shadow_1, openP):
            buylist.append(sec)

print(buylist)