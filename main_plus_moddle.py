import sys
sys.path.append('F:\GNanjing')
from fault_.fault_describe import X, S
from fault_.des import SS
from data_.model_one import result, DEVICECODE
from bayes_.bayes_model import end_result
from fuzzy_.fuzzy_model import weight, W_weight, s_mat_weight
from Oracle_.oracle import TestOracle
import numpy as np
import pandas as pd
import datetime

if __name__ == '__main__':
    '''模型一的输出'''
    result_cp = result.__deepcopy__()
    end_result_cp = end_result.__deepcopy__()
    print('\n模型一输出数据中存在的数据异常模式:\n', result)
    print('数据中存在的异常模式：')
    for i in result.T.index:
        # print(result[i].values[0])
        if result[i].values[0] == 1.0:
            print(X[i])
    '''模型二的输出'''
    print('\n模型二输出的故障类型及概率：\n', end_result)
    # print('最大值：', max(end_result.values[0]))
    max_value = max(end_result.values[0])
    broken_result = []  # 用来存放异常/故障的原因，S1-S17
    for i in end_result.columns:
        if float(max_value) == float(end_result[i]):
            broken_result.append(i)
            print('故障可能为{}:{}'.format(i,S[i]))
    '''模型三的输出'''
    result_dict = {}  # 用来存放模型三的结果
    for i in range(len(end_result)):
        # print(S_Probability.loc[i].values)
        columns = ['S3_0.0', 'S7_0.0', 'S8_0.0', 'S9_0.0', 'S10_0.0', 'S11_0.0', 'S12_0.0',
                   'S13_0.0', 'S14_0.0', 'S15_0.0', 'S16_0.0', 'S17_0.0']
        end_result = end_result[columns]
        w_weight = W_weight(s_mat_weight, end_result.loc[i].values)
        result = np.dot(w_weight, weight)
        print('\n模型三的评判结果：')
        '''0:正常 1：异常 2：故障'''
        # result_ = pd.DataFrame(result, index=['正常', '异常', '故障'], columns=['result'])
        result_dict = {'0': round(result[0], 4), '1': round(result[1], 4), '2': round(result[2], 4)}
        print(result_dict)
        state = max(result_dict, key=lambda x: result_dict[x])
        print('设备状态：', state)
        # print('设备状态：', str(result'''输出检测时间：dd/mm/yyyy格式'''_[result_.result == float(max(result_.values))].index.tolist()[0]))
    print('检测时间：', datetime.datetime.now())

    b_r = ' '.join(broken_result)  # 取出列表中的所有元素

    '''模型三结果存入数据库'''
    test_oracle = TestOracle('mw_app', 'app', '127.0.0.1', '1521', 'DBORCALE')
    # param=[('30M00000059982619','(正常：0.3；异常：0.5；故障：0.2)','异常',time.strftime("%Y/%m/%D %H:%M:%S")),]
    param = [(DEVICECODE, datetime.datetime.now(), state, b_r, result_dict['0'], result_dict['1'], result_dict['2']), ]
    param_1 = [
        (DEVICECODE, datetime.datetime.now(), int(result_cp.iloc[0, 0]), int(result_cp.iloc[0, 1]),
         int(result_cp.iloc[0, 2]),
         int(result_cp.iloc[0, 3]),
         int(result_cp.iloc[0, 4]), int(result_cp.iloc[0, 5]), int(result_cp.iloc[0, 6]), int(result_cp.iloc[0, 7]),
         int(result_cp.iloc[0, 8])), ]
    param_2 = [(DEVICECODE, datetime.datetime.now(), float(end_result_cp.iloc[0, 0]), float(end_result_cp.iloc[0, 1]),
                float(end_result_cp.iloc[0, 2]), float(end_result_cp.iloc[0, 3]), float(end_result_cp.iloc[0, 4]) \
                    , float(end_result_cp.iloc[0, 5]), float(end_result_cp.iloc[0, 6]), float(end_result_cp.iloc[0, 7]),
                float(end_result_cp.iloc[0, 8]), float(end_result_cp.iloc[0, 9]) \
                    , float(end_result_cp.iloc[0, 10]), float(end_result_cp.iloc[0, 11]), float(end_result_cp.iloc[0, 12]),
                float(end_result_cp.iloc[0, 13]), float(end_result_cp.iloc[0, 14]) \
                    , float(end_result_cp.iloc[0, 15]), float(end_result_cp.iloc[0, 16]),
                SS['S1'], SS['S2'], SS['S3'], SS['S4'], SS['S5'], SS['S6'], SS['S7'], SS['S8'],
                SS['S9'], SS['S10'], SS['S11'], SS['S12'], SS['S13'], SS['S14'], SS['S15'],
                SS['S16'], SS['S17']), ]
    sql_insert = 'insert into BHT_DEVICE_STATUS(DEVICECODE,TIME,DEVICE_STATUS,BROKEN_RESULT,STATUS_0,STATUS_1,STATUS_2)values(:1,:2,:3,:4,:5,:6,:7)'
    sql_insert_1 = 'insert into BHT_DEVICE_MIDDLE_PARTONE(DEVICECODE,TIME,DEVICE_OBNORMAL_X1,DEVICE_OBNORMAL_X2,DEVICE_OBNORMAL_X3,DEVICE_OBNORMAL_X4,DEVICE_OBNORMAL_X5,DEVICE_OBNORMAL_X6,DEVICE_OBNORMAL_X7,DEVICE_OBNORMAL_X8,DEVICE_OBNORMAL_X9)values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)'
    sql_insert_2 = 'insert into BHT_DEVICE_MIDDLE_PARTTWO(DEVICECODE,TIME,DEVICE_FAULT_S1,DEVICE_FAULT_S2,DEVICE_FAULT_S3,DEVICE_FAULT_S4,DEVICE_FAULT_S5,DEVICE_FAULT_S6,DEVICE_FAULT_S7,DEVICE_FAULT_S8,DEVICE_FAULT_S9,\
                            DEVICE_FAULT_S10,DEVICE_FAULT_S11,DEVICE_FAULT_S12,DEVICE_FAULT_S13,DEVICE_FAULT_S14,DEVICE_FAULT_S15,DEVICE_FAULT_S16,DEVICE_FAULT_S17,\
                            DEVICE_FAULT_S1_DATA_RESULT,DEVICE_FAULT_S2_DATA_RESULT,DEVICE_FAULT_S3_DATA_RESULT,DEVICE_FAULT_S4_DATA_RESULT,DEVICE_FAULT_S5_DATA_RESULT, \
                           DEVICE_FAULT_S6_DATA_RESULT,DEVICE_FAULT_S7_DATA_RESULT,DEVICE_FAULT_S8_DATA_RESULT,DEVICE_FAULT_S9_DATA_RESULT,DEVICE_FAULT_S10_DATA_RESULT,\
                           DEVICE_FAULT_S11_DATA_RESULT,DEVICE_FAULT_S12_DATA_RESULT,DEVICE_FAULT_S13_DATA_RESULT,DEVICE_FAULT_S14_DATA_RESULT,DEVICE_FAULT_S15_DATA_RESULT,\
                           DEVICE_FAULT_S16_DATA_RESULT,DEVICE_FAULT_S17_DATA_RESULT)values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21\
                           ,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35,:36)'

    # param = [(DEVICECODE, state, b_r, result_dict['0'], result_dict['1'], result_dict['2']), ]
    try:
        '''插入数据'''
        # sql_insert = 'insert into BHT_DEVICE_STATUS(DEVICECODE,DEVICE_STATUS,BROKEN_RESULT,STATUS_0,STATUS_1,STATUS_2)values(:1,:3,:4,:5,:6,:7)'
        test_oracle.insert(sql_insert, param)

    except:
        print('最终表插入失败')
    test_oracle = TestOracle('mw_app', 'app', '127.0.0.1', '1521', 'DBORCALE')
    try:
        test_oracle.insert(sql_insert_1, param_1)
    except:
        print('中间表一插入失败')
    test_oracle = TestOracle('mw_app', 'app', '127.0.0.1', '1521', 'DBORCALE')
    try:
        test_oracle.insert(sql_insert_2, param_2)
    except:
        print('中间表二插入失败')