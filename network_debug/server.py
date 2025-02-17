import socket

# 创建接收端 socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定到本地地址和端口
receiver_socket.bind(('localhost', 12345))

# 开始监听连接
receiver_socket.listen(1)
print("等待连接...")

# 等待连接
client_socket, client_address = receiver_socket.accept()
print(f"已连接到 {client_address}")

# 接收消息
message = client_socket.recv(1024)
print("接收到消息:", message.decode())

# 向发送端发送响应
client_socket.sendall(b'Hello, Sender!')

# 关闭连接
client_socket.close()
receiver_socket.close()
