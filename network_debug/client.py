import socket
import time
import random
from neuracle_lib.dataServer import DataServerThread

def run_eeg_receiver():
    time.sleep(3)
    return int(random.random()>0.5)

HOST = "127.0.0.1"
PORT = 12345

# 创建 TCP 连接
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("已连接到 Unity")

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
            ret=run_eeg_receiver() # 0 for left,1 for right

        if ret==0:
            client_socket.sendall("l".encode("utf-8"))
        elif ret==1:
            client_socket.sendall("r".encode("utf-8"))
        else:
            print("未知结果")
        print(f"结果为{ret}，已发送给Unity")
except KeyboardInterrupt:
    print("\n连接关闭")
finally:
    client_socket.close()

