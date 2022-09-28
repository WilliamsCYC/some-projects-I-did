import os
import pandas as pd

def Open_data():
    path = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份'

    # 获取全部备份数据文件夹名称
    data_list = os.listdir(path)

    n = 1
    data_dic = {}
    files = ''
    for i in data_list:
        if n <= 9:
            files += str(n) + ' : ' + i + '\n'
        else:
            files += str(n) + ': ' + i + '\n'
        data_dic[str(n)] = i
        n += 1

    file = input(files + '\n' + '请输入目标数据对应的数字编号：' + '\n')

    dir_name = data_dic[file]

    data_name = path + '\\' + dir_name + '\\' + 'data' + dir_name + '.csv'
    whole_list_name = path + '\\' + dir_name + '\\' + 'whole_list' + dir_name + '.csv'

    f = open(whole_list_name, encoding='UTF-8')
    whole_list = pd.read_csv(f)

    whole_list = whole_list.drop(['Unnamed: 0'], axis=1)
    whole_list = list(whole_list.iloc[:, 0])

    f = open(data_name, encoding='UTF-8')
    data = pd.read_csv(f)
    data = data.drop(data[data['open']==0].index)

    return whole_list, data