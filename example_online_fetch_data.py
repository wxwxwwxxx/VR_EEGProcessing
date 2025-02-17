
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# Author: FANG Junying, fangjunying@neuracle.cn

# Versions:
# 	v0.1: 2018-08-14, orignal
# 	v1.0: 2020-06-04，update demo
# Copyright (c) 2016 Neuracle, Inc. All Rights Reserved. http://neuracle.cn/

from neuracle_lib.dataServer import DataServerThread
import time
import numpy as np
import matplotlib.pyplot as plt
def main():
    ## 配置设备
    neuracle = dict(device_name='Neuracle', hostname='127.0.0.1', port=8712,
                    srate=1000, chanlocs=['Pz', 'POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2', 'TRG'], n_chan=27)

    dsi = dict(device_name='DSI-24', hostname='127.0.0.1', port=8844,
               srate=300,
               chanlocs=['P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'CM', 'A1', 'Fp1', 'Fp2', 'T3', 'T5', 'O1',
                         'O2', 'X3', 'X2', 'F7', 'F8', 'X1', 'A2', 'T6', 'T4', 'TRG'], n_chan=25)
    neuroscan = dict(device_name='Neuroscan', hostname='127.0.0.1', port=4000,
                     srate=1000,
                     chanlocs=['Pz', 'POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2', 'TRG'] + ['TRG'], n_chan=65)
    device = [neuracle, dsi, neuroscan]
    ### 选着设备型号,默认Neuracle
    target_device = device[0]
    ## 初始化 DataServerThread 线程
    time_buffer = 3 # second
    thread_data_server = DataServerThread(device=target_device['device_name'], n_chan=target_device['n_chan'],
                                          srate=target_device['srate'], t_buffer=time_buffer)


    '''
    在线数据获取演示：每隔一秒钟，获取数据（数据长度 = time_buffer）
    '''
    N, flagstop = 0, False
    # last_n_update = -1
    try:
        while not flagstop:  # get data in one second step
            nUpdate = thread_data_server.GetDataLenCount()
            # if nUpdate != last_n_update:
            #     print(nUpdate)
            #     last_n_update = nUpdate
            d = thread_data_server.GetBufferData()
            print(d[0,-1])
            if nUpdate > (time_buffer * target_device['srate'] - 1):
                N += 1
                data = thread_data_server.GetBufferData()
                thread_data_server.ResetDataLenCount()
                # triggerChan = data[-1,:]
                # idx = np.argwhere(triggerChan!=0)

                # 生成横轴数据
                x = np.arange(3000)

                # 创建折线图
                plt.figure(figsize=(10, 5))

                plt.plot(x, data[0]/100000.0, label=f'Vector {0}')
                plt.plot(x, data[2]/100000.0, label=f'Vector {2}')
                plt.plot(x, data[26], label=f'Vector {26} (TRG)')
                # 添加标签和图例
                plt.xlabel('X-axis (3000 points)')
                plt.ylabel('Values')
                plt.title('Selected Vectors from Array')
                plt.legend()
                plt.grid()

                # 显示图像
                plt.show()

    except:
        pass
    ## 结束线程
    thread_data_server.stop()
# 在线是微V，离线是V
if __name__ == '__main__':
   main()

