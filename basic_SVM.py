# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# Versions:
# 	v0.1: 2018-08-14, orignal

# Author: FANG Junying, fangjunying@neuracle.cn
# Copyright (c) 2016 Neuracle, Inc. All Rights Reserved. http://neuracle.cn/

from neuracle_lib.readbdfdata import readbdfdata,readdatalabel

import os
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import numpy as np
from preprocess import preprocess_all,extract_feature

def preprocess_for_data_label(data,label,data_length = 3000):
    data = [preprocess_all(i,lowcut=7.0,highcut=35.0) for i in data]
    # 去除不满足要求的index
    invalid_index = [i for i, x in enumerate(data) if x.shape[1] != data_length]
    for i in sorted(invalid_index, reverse=True):
        del data[i]
        del label[i]
    # all_data = [extract_feature(i,sf,z_score=False) for i in all_data]
    data = np.stack(data, axis=0)
    data = data.reshape(data.shape[0],-1)
    label = np.array(label)
    return data,label
def check_files_format(path):
    filename = []
    pathname = []
    if len(path) == 0:
        raise TypeError('please select valid file')

    elif len(path) == 1:
        (temppathname, tempfilename) = os.path.split(path[0])
        if 'edf' in tempfilename:
            filename.append(tempfilename)
            pathname.append(temppathname)
            return filename, pathname
        elif 'bdf' in tempfilename:
            raise TypeError('unsupport only one neuracle-bdf file')
        else:
            raise TypeError('not support such file format')

    else:
        temp = []
        temppathname = r''
        evtfile = []
        idx = np.zeros((len(path) - 1,))
        for i, ele in enumerate(path):
            (temppathname, tempfilename) = os.path.split(ele)
            if 'data' in tempfilename:
                temp.append(tempfilename)
                if len(tempfilename.split('.')) > 2:
                    try:
                        idx[i] = (int(tempfilename.split('.')[1]))
                    except:
                        raise TypeError('no such kind file')
                else:
                    idx[i] = 0
            elif 'evt' in tempfilename:
                evtfile.append(tempfilename)

        pathname.append(temppathname)
        datafile = [temp[i] for i in np.argsort(idx)]

        if len(evtfile) == 0:
            raise TypeError('not found evt.bdf file')

        if len(datafile) == 0:
            raise TypeError('not found data.bdf file')
        elif len(datafile) > 1:
            print('current readbdfdata() only support continue one data.bdf ')
            return filename, pathname
        else:
            filename.append(datafile[0])
            filename.append(evtfile[0])
            return filename, pathname


if __name__ == '__main__':
    # root = Tk()
    # root.withdraw()
    # sf = 1000
    # filename = ['data.bdf', 'evt.bdf']
    # pathname = [r'C:\Program Files (x86)\Neuracle\Neusen W\Data\2025\01\17日下午第三次_全部有效',r'C:\Program Files (x86)\Neuracle\Neusen W\Data\2025\01\17日下午第二次_全部有效']
    # eeg = readbdfdata(filename, pathname)
    # edata = eeg["data"]
    # anno = eeg["events"]
    # mi26_channel_list = ["FCz","FC1","FC2","FC3","FC4","FC5","FC6","FT7","FT8","Cz","C1","C2","C3","C4","C5","C6","T7","T8","CP1","CP2","CP3","CP4","CP5","CP6","TP7","TP8"]
    # all_ch_names = eeg["ch_names"]
    # mi26_channel_index = [all_ch_names.index(i) for i in mi26_channel_list]
    # all_data = []
    # all_label = []
    # for i in anno:
    #     time_marker = i[0]
    #     label = i[2]-1
    #     all_data.append(edata[mi26_channel_index,time_marker+500:time_marker+3500])
    #     all_label.append(label)
    all_data,all_label = readdatalabel(
        [r'C:\Program Files (x86)\Neuracle\Neusen W\Data\2025\01\17日下午第二次_全部有效',
         r"C:\Program Files (x86)\Neuracle\Neusen W\Data\2025\01\17日下午第三次_全部有效",
         r"C:\Program Files (x86)\Neuracle\Neusen W\Data\2025\01\17日下午第四次_全部有效"])
    all_data_np,all_label_np = [],[]
    for d,l in zip(all_data,all_label):
        d,l = preprocess_for_data_label(d,l)
        all_data_np.append(d)
        all_label_np.append(l)

    param_grid = {
        'C': [0.1, 1, 10, 100],
        'kernel': ['linear', 'rbf'],
        'gamma': [0.001, 0.01, 0.1, 1, 10]
    }
    # 划分训练集和测试集
    X_train, y_train = np.concatenate(all_data_np[0:2]),np.concatenate(all_label_np[0:2])
    X_test, y_test = all_data_np[2],all_label_np[2]
    # print(X_train.shape,y_train.shape,X_test.shape,y_test.shape)
    # X_train, X_test, y_train, y_test = train_test_split(all_data, all_label, test_size=0.3, random_state=42)
    # 创建 SVM 模型
    # model = svm.SVC(kernel='rbf')
    grid = svm.SVC()
    # # 执行网格搜索
    grid_search = GridSearchCV(grid, param_grid, cv=10, scoring='accuracy')

    grid_search.fit(X_train, y_train)
    print("最佳参数:", grid_search.best_params_)
    print("最佳得分:", grid_search.best_score_)
    model = grid_search.best_estimator_
    # 测试模型
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    # 输出结果
    accuracy_train = accuracy_score(y_train, y_train_pred)
    # 测试模型
    y_pred = model.predict(X_test)
    # 输出结果
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Train acc={accuracy_train}, Test acc={accuracy}")