import numpy as np
from outliers import smirnov_grubbs as grubbs
from Oracle_.oracle import TestOracle
from fault_.fault_describe import univariate
import pandas as pd
from datetime import datetime,timedelta
import copy

'''从数据库中获取数据'''
# connect参数  用户名、密码、host地址：端口、服务名
test_oracle=TestOracle('mw_app','app','127.0.0.1','1521','DBORCALE')
print("连接成功")


'''不同监测类型，对应的数据还没有找到，到时候需要改的数据为：

MONITORINGDATATABLE

替换为应有的数据就行。
'''



'''查数据'''
sql_select = 'select DEVICECODE,TYPENAME,MONITORINGDATATABLE from BHV_DEVICE'
data_oracle= test_oracle.select(sql_select)
for i in data_oracle:
    if univariate[i['TYPENAME']]=='none':
        print('{}表中不存在数据'.format(univariate[i['TYPENAME']]))
        continue
    try:
        aDay = timedelta(days=10)
        date_1 = '2020-03-11';date_one=datetime.strptime(date_1,"%Y-%m-%d")
        date_2 = date_one-aDay;date_2=date_2.strftime("%Y-%m-%d")
        # sql_select_two = "select {} from {} t where t.RESAVE_TIME between date '{}' and date '{}' order by t.RESAVE_TIME and where t.DEVICECODE = '{}'"
        sql_select_two = "select {} from {} t where t.DEVICECODE = '{}' and t.RESAVE_TIME between date '{}' and date '{}' order by t.RESAVE_TIME asc"
        sql_select_two = sql_select_two.format(univariate[i['TYPENAME']],i['MONITORINGDATATABLE'],i['DEVICECODE'],date_2,date_1)
        data_oracle_two = pd.DataFrame(test_oracle.select(sql_select_two))
        if data_oracle_two.empty==True:
            print('{}表为空'.format(univariate[i['TYPENAME']]))
        else:
            print(data_oracle_two)
            print('***********************')
    except:
        print("设备标号为{}，监测类型为{}，数据库表为{}，发生故障".format(i['DEVICECODE'],i['TYPENAME'],i['MONITORINGDATATABLE']))
    # break
# print(data_oracle)
# DEVICECODE = data_oracle['DEVICECODE'][0]
# print('DEVICECODE ：',DEVICECODE)
# print(data_oracle)

