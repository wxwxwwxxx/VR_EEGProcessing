

#
# import RPi.GPIO as GPIO
# import threading
import time
def startMotor(kit_handler):
    kit_handler.servo[0].angle = 180
    kit_handler.servo[1].angle = 180
    kit_handler.servo[2].angle = 180
    kit_handler.servo[3].angle = 180
    kit_handler.servo[4].angle = 180
    kit_handler.servo[5].angle = 180
    time.sleep(0.2)
def endMotor(kit_handler):
    print("Ending...")
    kit_handler.servo[0].angle = 180
    kit_handler.servo[1].angle = 180
    kit_handler.servo[2].angle = 180
    kit_handler.servo[3].angle = 180
    kit_handler.servo[4].angle = 0
    kit_handler.servo[5].angle = 0
    time.sleep(2)
    kit_handler.servo[0].angle = 0
    kit_handler.servo[1].angle = 0
    kit_handler.servo[2].angle = 0
    kit_handler.servo[3].angle = 0
    print("End motor.")
def pauseMotor(kit_handler):
    kit_handler.servo[0].angle = 180
    kit_handler.servo[1].angle = 180
    kit_handler.servo[2].angle = 180
    kit_handler.servo[3].angle = 180
    kit_handler.servo[4].angle = 0
    kit_handler.servo[5].angle = 0
def setStatus(bs,hand,kit_handler):
    if bs == "b":
        kit_handler.servo[0].angle = 0
        kit_handler.servo[1].angle = 180
    elif bs == "s":
        kit_handler.servo[0].angle = 180
        kit_handler.servo[1].angle = 0
    if hand == "l":
        kit_handler.servo[2].angle = 180
        kit_handler.servo[3].angle = 0
    elif hand == "r":
        kit_handler.servo[2].angle = 0
        kit_handler.servo[3].angle = 180
    elif hand == "a":
        kit_handler.servo[2].angle = 180
        kit_handler.servo[3].angle = 180


# GPIO.setmode(GPIO.BCM)
# kit = ServoKit(channels=16)  # 初始化 16 路 PWM 控制器
#
# try:
#     startMotor(kit)
# finally:
#     endMotor(kit)
#     GPIO.cleanup()