import RPi.GPIO as GPIO
import threading
import socketserver
import time
from contextlib import closing
from LEDController import LEDController
from adafruit_servokit import ServoKit
from pca9865 import *
# -------------------------
# TCP Server Handler
# -------------------------
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # 记录连接
        print(f"[+] 客户端连接：{self.client_address}")
        with client_set_lock:
            client_set.add(self.request)
            led_con.on()
        try:
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                glove_event.set()
                hand[0] = data.decode(errors='ignore')
                print(f"[客户端消息] {self.client_address} 说：{hand[0]}")
        finally:
            print(f"[-] 客户端断开：{self.client_address}")
            with client_set_lock:
                client_set.discard(self.request)
                if len(client_set) == 0:
                    led_con.blink()
            with closing(self.request):
                pass

def motor_handler():
    while True:
        glove_event.wait()
        startMotor(kit)
        if hand[0] == "l":
            led_l.blink()
            setStatus("b", hand[0], kit)
            time.sleep(2)
            setStatus("s", hand[0], kit)
            time.sleep(2)
            led_l.off()
        elif hand[0]=="r":
            led_r.blink()
            setStatus("b", hand[0], kit)
            time.sleep(2)
            setStatus("s", hand[0], kit)
            time.sleep(2)
            led_r.off()
        pauseMotor(kit)
        glove_event.clear()
# -------------------------
# 主程序入口
# -------------------------
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 13579  # 监听所有 IP
    GPIO.setmode(GPIO.BCM)
    led_con = LEDController(gpio_pin=16, blink_interval=0.5)
    led_l = LEDController(gpio_pin=20, blink_interval=0.3)
    led_r = LEDController(gpio_pin=21, blink_interval=0.3)
    kit = ServoKit(channels=16)  # 初始化 16 路 PWM 控制器
    glove_event = threading.Event()
    client_set = set()
    client_set_lock = threading.Lock()
    hand=[""]
    try:
        print("[*] 初始化电伺服程序 ...")
        thread = threading.Thread(target=motor_handler)
        thread.daemon = True  # 后台线程
        thread.start()
        print("[*] 启动 TCP Server 中...")
        server = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"[+] TCP Server 已启动：{HOST}:{PORT}")
        # 启动初始状态
        led_con.blink()
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] 中断退出")
    finally:
        server.shutdown()
        server.server_close()
        endMotor(kit)
        led_con.cleanup()
        led_r.cleanup()
        led_l.cleanup()
        GPIO.cleanup()
