import tushare as ts
import pandas as pd
import datetime
import os

choice = input('请选择获取方式：a.指定起止日期 b.指定结束日期和天数' + '\n')

# tushare基本配置
ts.set_token('')
pro = ts.pro_api()
pro = ts.pro_api('')

# 获取全A股列表
whole_list = pro.stock_basic()
whole_list = whole_list['ts_code'].tolist()

if choice == 'a':
    start_date = str(input('请输入开始日期，格式为YYYYMMDD' + '\n'))
    end_date = str(input('请输入结束日期，格式为YYYYMMDD' + '\n'))
    calendar = pd.bdate_range(start_date, end_date).date

    print(calendar)

    lens = len(whole_list) // 1000 + 1

    data = pd.DataFrame({
        'ts_code': [],
        'trade_date': [],
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'pre_close': [],
        'change': [],
        'pct_chg': [],
        'vol': [],
        'amount': []
    })

    for i in range(lens):
        list = ','.join(whole_list[i * 1000: (i + 1) * 1000])
        for j in calendar:
            j = j.strftime('%Y%m%d')
            data_part = pro.daily(ts_code=list, start_date=j, end_date=j)
            data = data.append(data_part)

    data = data.set_index('trade_date').sort_index()

    # 创建文件夹
    dir_path = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份\\'
    dir_name = '(' + start_date + '-' + end_date + ')'
    os.mkdir(dir_path + dir_name)

    # 数据存储
    whole_list_file = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份\\' + dir_name + '\\' + 'whole_list' + '(' + start_date + '-' + end_date + ')' + '.csv'
    data_file = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份\\' + dir_name + '\\' + 'data' + '(' + start_date + '-' + end_date + ')' + '.csv'

    whole_list_save = pd.DataFrame(whole_list)
    whole_list_save.to_csv(whole_list_file, sep=',')
    data.to_csv(data_file, sep=',')

elif choice == 'b':
    end_date = str(input('请输入结束日期，格式为YYYYMMDD' + '\n'))
    period = int(input('请输入天数' + '\n'))

    start_date = datetime.datetime.strptime(end_date, '%Y%m%d') - datetime.timedelta(days=period-1)

    start_date = start_date.strftime('%Y%m%d')

    calendar = pd.bdate_range(start_date, end_date).date

    lens = len(whole_list) // 1000 + 1

    data = pd.DataFrame({
        'ts_code': [],
        'trade_date': [],
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'pre_close': [],
        'change': [],
        'pct_chg': [],
        'vol': [],
        'amount': []
    })

    for i in range(lens):
        list = ','.join(whole_list[i * 1000: (i + 1) * 1000])
        for j in calendar:
            j = j.strftime('%Y%m%d')
            data_part = pro.daily(ts_code=list, start_date=j, end_date=j)
            data = data.append(data_part)

    data = data.set_index('trade_date').sort_index()

    # 创建文件夹
    dir_path = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份\\'
    dir_name = '(' + start_date + '-' + end_date + ')'
    os.mkdir(dir_path + dir_name)

    # 数据存储
    whole_list_file = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份\\' + dir_name + '\\' + 'whole_list' + '(' + start_date + '-' + end_date + ')' + '.csv'
    data_file = 'C:\\Users\\Williams\\Desktop\\Coding\\股票K线数据处理\\数据备份\\' + dir_name + '\\' + 'data' + '(' + start_date + '-' + end_date + ')' + '.csv'

    whole_list_save = pd.DataFrame(whole_list)
    whole_list_save.to_csv(whole_list_file, sep=',')
    data.to_csv(data_file, sep=',')

else:
    print('请输入小写a或者b')