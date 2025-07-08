import time
import random
import socket
from neuracle_lib.dataServer import DataServerThread
from sklearn import svm
import joblib
from EEG_preprocess import preprocess_all
pos_dict = {"p":0,"v":0}
def run_eeg_receiver():
    time.sleep(3)
    return int(random.random()>0.5)
def eeg_init():
    neuracle_MI26 = dict(device_name='Neuracle', hostname='127.0.0.1', port=8712,
                    srate=1000, chanlocs=['Pz', 'POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2', 'TRG'], n_chan=27)
    time_buffer = 3  # second, fixed
    target_device = neuracle_MI26
    thread_data_server = DataServerThread(device=target_device['device_name'], n_chan=target_device['n_chan'],
                                          srate=target_device['srate'], t_buffer=time_buffer)
    ### 建立TCP/IP连接
    notconnect = thread_data_server.connect(hostname=target_device['hostname'], port=target_device['port'])
    if notconnect:
        raise TypeError("Can't connect recorder, Please open the hostport ")
    else:
        # 启动线程
        thread_data_server.Daemon = True
        thread_data_server.start()
        print('Data server connected')
    return thread_data_server
def load_model(path):
    model = joblib.load(path)
    return model

# def run_eeg_result(thread_data_server,model):
#     thread_data_server.ResetDataLenCount()
#     while True:
#         nUpdate = thread_data_server.GetDataLenCount()
#         if nUpdate > (3 * thread_data_server.srate - 1):
#             data = thread_data_server.GetBufferData()
#             break
#     data = data[0:26]/1000000.0 # no TRG channel
#     data = preprocess_all(data)
#     data = data.reshape([-1])[None,...]
#     ret = model.predict(data)[0]
#     return ret
def run_eeg_result(thread_data_server,model):
    # for debug purpose
    if pos_dict["p"]==-4:
        pos_dict["v"]=1
    elif pos_dict["p"]==4:
        pos_dict["v"]=0
    ret = pos_dict["v"]
    if ret == 0:
        pos_dict["p"] -= 1
    elif ret == 1:
        pos_dict["p"] += 1
    time.sleep(3)
    return ret
def connect_to_server(host,port,retry):
    if not retry:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            return client_socket
        except socket.error as e:
            print(f"Failed to connect to server {host}:{port}: {e}, returning None. ")
            return None
    else:
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                client_socket.connect((host, port))
                return client_socket
            except socket.error as e:
                print(f"Failed to connect to server {host}:{port}: {e}, retrying. ")
                time.sleep(3)

UNITY_HOST = "127.0.0.1"
UNITY_PORT = 12345
print(f"准备连接Unity服务端,IP:{UNITY_HOST},PORT:{UNITY_PORT}")
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((UNITY_HOST, UNITY_PORT))
client_socket = connect_to_server(UNITY_HOST,UNITY_PORT,True)
print("已连接到 Unity")

GLOVE_HOST = "192.168.1.108"
GLOVE_PORT = 13579
print(f"准备连接手套服务端,IP:{GLOVE_HOST},PORT:{GLOVE_PORT}")
glove_client_socket = connect_to_server(GLOVE_HOST,GLOVE_PORT,False)
if glove_client_socket:
    print(f"手套服务端连接成功")
else:
    print(f"手套服务端连接失败,忽略手套端")
# print(f"准备连接EEG服务端")
# dataserver = eeg_init()
# print("已连接到EEG服务端")
# model = joblib.load(r"model\zdn_model_250221.pkl")
dataserver = None
model = None
ret = None
try:
    while True:
        print("等待游戏Go指令")
        # 发送数据到 Unity
        # 接收来自 Unity 的消息

        received_data = client_socket.recv(1024)
        if not received_data:
            break

        if received_data.decode("utf-8") == "go":
            print("Go！")
            ret=run_eeg_result(dataserver,model)# 0 for left,1 for right
        if ret==0:
            client_socket.sendall("l".encode("utf-8"))

            if glove_client_socket:
                glove_client_socket.sendall("l".encode("utf-8"))
        elif ret==1:
            client_socket.sendall("r".encode("utf-8"))
            if glove_client_socket:
                glove_client_socket.sendall("r".encode("utf-8"))
        else:
            print("未知结果")
        print(f"结果为{ret}，已发送给Unity")
except KeyboardInterrupt:
    print("\n连接关闭")
finally:
    client_socket.close()

