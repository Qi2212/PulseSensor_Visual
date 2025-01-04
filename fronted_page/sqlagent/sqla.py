import pymysql
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Xsq031124',
    'database': 'pk_project',
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
            sql = "SELECT filename,BPM,IBI,Pulse,is_normal FROM detectionRecord ORDER BY time DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                pulse_info = result
            pulse_info = f"测量者{result['username']}的心率测量记录如下: BPM(每分钟心脏跳动次数):{result['BPM']},Pulse(每毫秒):{result['Pulse']},检测时间:{result['time']},测量数据在理论范围是否正常:{result['is_normal']}"
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()
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

def sql_Agent_pulse(prompt,available_functions):
    prompt = prompt
    message = [{"role":"user","content":prompt}]

    response = client.chat.completions.create(
    model="glm-4-plus",  
    messages= message,
    tools =tools,
    tool_choice = "auto"
)
    #找出相应的函数
    function_to_call = available_functions[response.choices[0].message.tool_calls[0].function.name]
    function_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    fucntion_response = function_to_call(**function_args)

    message.append({
        "role":"tool",
        "name":response.choices[0].message.tool_calls[0].function.name,
        "content":"最近一次检测记录的信息："+str(fucntion_response)
    })
    return message