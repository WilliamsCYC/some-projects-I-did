from Data_Process import *
from Open_Data import *
from Judge import *


# 导入数据
whole_list, data = Open_data()


# 策略主体

qi_ming_xing = []
yun_ping_chui = []
chui_zi = []
yun_shi_zi = []


for sec in whole_list:
    d_sec = data[data['ts_code'] == sec]
    d_sec = d_sec.set_index('trade_date').sort_index()
    if len(d_sec) < 25:
        continue

    close, openP, high, low, turn, body1, body2, body3, up_shadow_1, up_shadow_2, up_shadow_3, down_shadow_1, down_shadow_2, down_shadow_3, Pct_change_1, Pct_change_2, MA5, MA10, MA15, turn_MA10 = Get_all_Data(d_sec)

    # 启明星
    if judge_xia_die(MA5, MA10, MA15):
        q = np.array([judge_qi_d(close, openP, body2, turn, turn_MA10),
                      judge_qi_c(close, openP, body2),
                      judge_qi_b(close, openP, body2),
                      judge_qi_a(close, openP, body2)])
        if q.any() == 1:
            qi_ming_xing.append(sec)


    # 孕平锤
    if judge_xia_die(MA5, MA10, MA15):
        if judge_yun(1, openP, close):
            if judge_ping_tou(1, low, close):
                if judge_chui(1, body1, down_shadow_1, up_shadow_1, openP):
                    yun_ping_chui.append(sec)

    # 锤子
    if judge_xia_die(MA5, MA10, MA15):
        if judge_chui_zi(2, body2, down_shadow_2, up_shadow_2, openP, close, low, j=6):
            chui_zi.append(sec)

    # 孕十字
    if judge_xia_die(MA5, MA10, MA15):
        if judge_yun(1, openP, close) and judge_shi_zi(1, body1, down_shadow_1, openP):
            yun_shi_zi.append(sec)


print('-'*75)
if len(qi_ming_xing) + len(yun_ping_chui) + len(chui_zi) + len(yun_shi_zi) == 0:
    print('无结果')
else:
    if len(qi_ming_xing) > 0:
        print('启明星: ', len(qi_ming_xing), '\n', 'Stock:  ', ' '.join(qi_ming_xing), '\n')
    else:
        print('启明星: 无', '\n')
    if len(yun_ping_chui) > 0:
        print('孕平锤： ', len(yun_ping_chui), '\n', 'Stock:  ', ' '.join(yun_ping_chui), '\n')
    else:
        print('孕平锤： 无', '\n')
    if len(chui_zi) > 0:
        print('锤子： ', len(chui_zi), '\n', 'Stock:  ', ' '.join(chui_zi), '\n')
    else:
        print('锤子： 无', '\n')
    if len(yun_shi_zi) > 0:
        print('孕十字： ', len(yun_shi_zi), '\n', 'Stock:  ', ' '.join(yun_shi_zi))
    else:
        print('孕十字： 无')
print('-'*75)