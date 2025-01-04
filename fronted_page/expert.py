import streamlit as st
from zhipuai import ZhipuAI
import pymysql
import json

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Xsq031124',
    'database': 'sensor',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**db_config)


def pulse_detect():
    """
    检索数据库存储的最近一次的心率检测记录数据,给出详细的检测记录,包括测量人姓名,BPM(每分钟心脏跳动次数),Pulse(每毫秒),检测时间
    """
    try:
        #连接数据库
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "SELECT username,filename,BPM,IBI,Pulse,is_normal,time FROM detectionRecord ORDER BY time DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                pulse_info = result
            pulse_info = f"测量者{result['username']}的心率测量记录如下: BPM(每分钟心脏跳动次数):{result['BPM']},Pulse(每毫秒):{result['Pulse']},检测时间:{result['time']},测量数据在理论范围是否正常:{result['is_normal']}"
            print(pulse_info)
            return pulse_info
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    return pulse_info


tools = [
    {
        "type": "function",
        "function": {
            "name": "pulse_detect",
            "description": "检索数据库存储的最近一次的心率检测记录数据,给出详细的检测记录，包括测量人姓名，BPM(每分钟心脏跳动次数)，Pulse(每毫秒)，检测时间:{result['time']}",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

#工具函数传参
function_list = [pulse_detect]
available_functions = {func.__name__:func for func in function_list}

def sql_Agent_pulse(prompt,available_functions):
    prompt = prompt
    message = [{"role":"user","content":prompt}]
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
    model="glm-4-plus",  
    messages= message,
    tools =tools,
    tool_choice = "auto"
)   
    try:
        function_to_call = available_functions[response.choices[0].message.tool_calls[0].function.name]
        function_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        fucntion_response = function_to_call(**function_args)
        message.append({
        "role":"tool",
        "name":response.choices[0].message.tool_calls[0].function.name,
        "content":"最近一次检测记录的信息："+str(fucntion_response)
    })
        return message
    except Exception as e:
        print(f"{e}")
        return False



api_key = "0dfe4c124d9e14f2773216275f5ec7f8.FB35WYyZoKg92cD8"
st.set_page_config(page_title='TYUT - ChatGLM智能建议',  layout='wide', page_icon=':robot:')

st.title("💬 智能建议专家")
st.divider() 
st.caption("🚀 一个基于ChatGLM4的智能心率健康建议专家")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你可以向我询问有关健康方面的知识"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



def stream_out(messages):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
    model="glm-4-plus",  
    messages = messages,
    stream=True,)
    for chunk in response:
        bot_response = chunk.choices[0].delta.content
        yield str(bot_response)

#原始回答
def raw_stream_out(prompt):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
    model="glm-4-plus",  
    messages=[
        {"role": "user", "content": prompt},
    ],
    stream=True,
    )
    for chunk in response:
        bot_response = chunk.choices[0].delta.content
        yield str(bot_response)

if prompt := st.chat_input(f"Q:分析我最近一次的心率检并给出建议"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            message =  sql_Agent_pulse(prompt,available_functions) #append调用了我的agent的message
            print(message)
            if not message:
                print(prompt)
                response = raw_stream_out(prompt)
            else:
                response = stream_out(message)
            full_response = st.write_stream(response)
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message) #添加历史会话信息
