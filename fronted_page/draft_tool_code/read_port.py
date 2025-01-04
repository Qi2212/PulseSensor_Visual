import serial           
import sys
import re
import csv
import time 
import math
import os


def device_detection(port='COM3'):
    #所有可用的串口设备
    try:
        ser = serial.Serial(port, 115200, timeout=None) 
        ser_status=ser.is_open
        if ser_status:
            #串口状态
            print(f"串口{port}设备可用")
            ser.close()
            return True
        else:
            #设备状态不为True
            print(f"串口{port}设备不可用")
            ser.close()
            return False
    except Exception as e:
        print(f"检测串口设备状态遇到错误2:{e}")
        return False

def stop_detection(port='COM3'):
    pass


#语音模块的通信代码-->实现实时播报的通信
def sent_byte(message,port='COM6',bt=115200):
    try:
        ser = serial.Serial(port, 115200,timeout=1)
        while True:
            if ser.in_waiting > 0:
                time.sleep(0.1)
                ser.write(message.encode()) 
                break
            time.sleep(0.1)
        while True:
            if ser.in_waiting > 0:
                ser.flushOutput()
                ser.flushInput() 
                ser.write(b'E')
                ser.close() 
                break
            time.sleep(0.05)
               

    except Exception as e:
        print(f'打开串口遇到问题:{e}')
        return False
device_detection(port='COM6')
sent_byte()
print("检测设备状态:")
device_detection()
print("开始写数据:")
generate_csv_file()