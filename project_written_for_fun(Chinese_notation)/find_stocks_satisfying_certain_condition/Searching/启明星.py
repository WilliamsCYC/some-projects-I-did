from Data_Process import *
from Open_Data import *


whole_list, data = Open_data()


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


buylist = []

for sec in whole_list:
    d_sec = data[data['ts_code'] == sec]
    d_sec = d_sec.set_index('trade_date').sort_index()
    if len(d_sec) < 25:
        continue

    close, openP, high, low, turn, body1, body2, body3, up_shadow_1, up_shadow_2, up_shadow_3, down_shadow_1, down_shadow_2, down_shadow_3, Pct_change_1, Pct_change_2, MA5, MA10, MA15, turn_MA10 = Get_all_Data(d_sec)


    if judge_xia_die(MA5, MA10, MA15):
        if judge_qi_d(close, openP, body2, turn, turn_MA10):
            buylist.append(sec)
            print('d')
        if judge_qi_c(close, openP, body2):
            buylist.append(sec)
            print('c')
        if judge_qi_b(close, openP, body2):
            buylist.append(sec)
            print('b')
        if judge_qi_a(close, openP, body2):
            buylist.append(sec)
            print('a')

print(buylist)