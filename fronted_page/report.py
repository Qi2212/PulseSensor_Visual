import streamlit as st
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
import random
from db_config.db_info import get_latest_record
import os
st.title(':blue[开始体验]🔔')
st.markdown("""
## step4 检测结果
""")

placeholder = st.empty()
placeholder.markdown("校验检测结果")
st.divider() 
time.sleep(1)
t1 = random.randint(1,50)
placeholder.progress(0, "正在保存检测数据...")
time.sleep(1)
placeholder.progress(t1, "存入数据库...")
time.sleep(1)
#载入数据库数据
filename,BPM,IBI,Pulse,is_normal = get_latest_record()
if BPM =='未检测到数据':
    BPM = int(60000/IBI)
t2 = random.randint(t1+10,85)
placeholder.progress(t2, "正在保存检测数据...")
time.sleep(1)
placeholder.progress(100, "页面报告渲染...")
time.sleep(1.5)

#查找数据库最新生成的文件名并返回
main_path= r'D:\Users\Administrator\Desktop\sensor\data_saved'
file_path= os.path.join(main_path,filename)

data = pd.read_csv(file_path,encoding='gbk').iloc[0:-2,:]  
#最后一列时均值数据，不能读入
y1 = data['Pulse/mS']
y2 = data['IBI/mS']
x = [_ for _ in range(len(y1))]

if "df" not in st.session_state:
    st.session_state.df = data

    event = st.dataframe(
                        st.session_state.df,
                        key="data",
                        on_select="rerun",
                        selection_mode=["multi-row", "multi-column"],
                )
    event.selection 
            
                
pulse_fig1 = create_plotly_plot(x, y1,'Pulse/mS')
pulse_fig2 = create_plotly_plot(x, y2,'IBI/mS')
                
col1, col2 = st.columns(2)  
col1.plotly_chart(pulse_fig1, use_container_width=True)
col2.plotly_chart(pulse_fig2, use_container_width=True)

col1, col2,col3= st.columns(3)
col2.image(r"D:\Users\Administrator\Desktop\sensor\fronted_page\heart.png" ,width=350)
html_temp =f"""
        <div style="background-color:white;padding:13px;text-align:center;">
            <p style="font-family: 'Times New Roman', Times, serif; font-weight: bold; font-size: 20px; margin-top: 10px;">
                avg BPM(心率) 次/分钟:{BPM}<br>
                avg IBI/ms:{IBI}<br>
                avg Pulse/ms:{Pulse}<br>
                理论范围检测:{is_normal}
            </p>
        </div>
    """

st.markdown(html_temp, unsafe_allow_html = True) 

col1, col2,col3 = st.columns(3) 
with col2:
    st.page_link("expert.py", label="解读报告➡️(click me!)")





