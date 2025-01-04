import streamlit as st
#from draft_tool_code.read_port import device_detection
import serial           
import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import time
import threading
from matplotlib.animation import FuncAnimation  
from datetime import datetime
import subprocess
from draft_tool_code.read_port import device_detection
from plot_code.plot_dy import create_plotly_plot
import os
import serial           
import sys
import random

st.title(':blue[开始体验]🔔')
st.divider() 
st.markdown("""
    ## step3 开始检测
    """)
st.info(
        """
        请正确佩戴或穿戴设备,穿戴说明如下图所示|请确保您已正确佩戴传感器，否则会造成数据采集误差
        """
    )
col1, col2= st.columns(2)


col1.image(r"D:\Users\Administrator\Desktop\sensor\fronted_page\pic_static\light1.png", 
                    caption="指示灯闪烁",width=450)
col2.image(r"D:\Users\Administrator\Desktop\sensor\fronted_page\pic_static\sensor5.png",caption="指尖式佩戴示例",width=450)


st.subheader("请正确完成下述初始化检测相关配置🏃", divider="blue")
username = st.text_input(":red[*]您的姓名:")
st.divider()
low_Threshold = st.slider("心率时序图下界 (150-200):", 0, 100)


col1, col2, col3 = st.columns(3)
with col2:
    submit_button = st.button("提交&开始检测🏃")
if submit_button:
    ser = serial.Serial('COM6', 115200, timeout=1)
    placeholder = st.empty()
    placeholder.markdown("正在初始化硬件配置...")
    time.sleep(0.5)
    placeholder.progress(0, "正在连接JQ8900-16P")
    time.sleep(0.5)
    t1 = random.randint(40,60)
    placeholder.progress(t1, "正在连接Pulse Sensor")
    while True:
        if ser.in_waiting > 0:
            time.sleep(0.2)
            ser.write(b'S')  # 将字符串编码为字节并发送
            t2= random.randint(61,90)
            placeholder.progress(t2, "准备检测")
            ser.close()
            break
        time.sleep(0.1)
    params = [
        '--username', username,
        '--value_min', str(low_Threshold)]
    subprocess.run(["python", r"D:\Users\Administrator\Desktop\sensor\fronted_page\plot_code\plot_dy.py"]+ params)
    #关闭串口避免占用
    col1, col2,col3 = st.columns(3) 
    placeholder.progress(100, "检测完成")
    with col2:
        st.page_link("report.py", label="查看检测结果➡️(click me!)")



def generate_csv_file(port='COM3',bt=115200,username="Unknown"):
    try:
        ser = serial.Serial('COM3',115200, timeout=0)
        ser.write(b'S')
    except Exception as e:
        print(f'打开串口遇到问题:{e}')
        return False
