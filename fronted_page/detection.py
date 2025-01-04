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
from matplotlib.animation import FuncAnimation  # 用于创建动画效果，定期更新图表
from datetime import datetime
import subprocess
from draft_tool_code.read_port import device_detection
from plot_code.plot_dy import create_plotly_plot

st.set_page_config(page_title='TYUT - 实时检测',  layout='wide', page_icon=':bulb:')
st.title(':blue[开始体验]🔔')
st.divider() 
st.markdown("""
 ## step1 选择传感器
""")
option = st.selectbox(
    "选择要使用的传感器设备",
    ("PulseSensor", "JQ8900-16p(默认语音)"),
)
st.write(f"已选择",option)
st.markdown("""
 ## step2 设备就绪检测
""")
jc_button = st.button("检测设备", type="primary",icon="🚨")
if jc_button:
    if device_detection(port='COM3') and device_detection(port='COM6') :
        # #设备可用，撤销等待效果
        st.success('当前设备可以用，已就绪', icon="✅")
        col1, col2,col3 = st.columns(3) 
        with col2:
            st.page_link("dynamic_detect.py", label="实时检测➡️(click me!)")
    else:
        #设备不可以用提示用户稍后尝试
        st.error('当前设备不可用，请重试', icon="❌")

