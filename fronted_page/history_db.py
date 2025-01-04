import pymysql
from pymysql import cursors
import streamlit as st
import random
import pandas as pd
import streamlit as st
from db_config.db_info import fetch_mysql
import numpy as np
from db_config.db_info import get_record_count,calculate_column_IBI_mean,calculate_column_Pulse_mean
import os

st.title("历史检测记录")
st.divider() 
st.success('心率，即心脏每分钟跳动的次数，也称为安静心率，是评估心脏功能的基本指标之一。正常人的心率在安静状态下通常为60～100次/分。心率的变化可以受到多种因素的影响，包括年龄、性别、运动状态、情绪以及疾病等', icon="ℹ️")
st.info('检测注意：心率检查的注意事项包括保持饮食清淡、情绪平稳、睡眠充足，避免剧烈运动，穿着宽松，遵循医生指导，并特别注意检查前后的特殊要求，以确保检查结果的准确性', icon="ℹ️")
st.error('偏高提示：排除生理因素，常见于心律失常、发热、甲亢、贫血、休克、心肌缺血、充血性心力衰竭，以及使用肾上腺素、阿托品等药物', icon="ℹ️")
st.error('偏低提示：排除生理因素，常见于心肌梗死、颅内疾病、严重缺氧、低温、甲减、阻塞性黄疸和血管迷走神经晕厥，以及拟胆碱药物、胺碘酮、β受体阻滞剂等药物也会引起心率偏低', icon="ℹ️")

main_path= r'D:\Users\Administrator\Desktop\sensor\data_saved'
result = fetch_mysql()
history_df = pd.DataFrame(result)

pulse_values = []
for index, filename in enumerate(history_df['filename']):
    file_path = os.path.join(main_path, filename)
    data_pulse = pd.read_csv(file_path, encoding='gbk')
    pulse_value = data_pulse["Pulse/mS"].tolist()
    print(type(pulse_value))
    pulse_values.append(pulse_value)

pulse_series = pd.Series(pulse_values, index=history_df.index)
history_df['plot'] = pulse_series

st.dataframe(
        history_df,
        column_config={
            "id": "检测序号",
            "time": "检测日期",
            "sensor": "传感器型号",
            "filname": "检测数据文件名",
            "plot":st.column_config.LineChartColumn("Pulse mS", y_min=200, y_max=700)
        },
        hide_index=True,
    )

