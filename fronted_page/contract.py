import streamlit as st
import re 
from db_config.db_info import insert_mysql_feedback
st.set_page_config(page_title='TYUT - 问题反馈',  layout='wide', page_icon=':thought_balloon:')
st.title("问题反馈")
st.divider() 
st.title("技术人员正在马不停蹄地debug:blue[!] :sunglasses:")
#提交邮箱格式校验
email_regex = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)
multi = '''
* 前端支持：周思语 :ok_woman: |  韩鑫 :runner: |  夏书淇 :speech_balloon:
* 后端支持：夏书淇 :speech_balloon: |  周思语 :ok_woman: |  韩鑫 :runner: 
* 传感器技术支持：韩鑫 :runner: |  夏书淇 :speech_balloon: |  周思语 :ok_woman:
* [排名不分先后 :yum:]
'''
st.markdown(multi)
with st.expander("联系我们"):
    with st.form(key='contact', clear_on_submit=True):
        email = st.text_input('联系邮箱')
        problem_description = st.text_area("遇到问题", "请将您遇到的问题填写在此处以便我们能及时解决")
        submit_button = st.form_submit_button(label='发送信息')
    if submit_button:
        # 校验邮箱地址格式
        if not email_regex.match(email):
            st.error("请输入有效的邮箱地址。")
            # 校验问题描述是否为空
        elif not problem_description.strip():
            st.error("问题描述不能为空。")
        else:
            insert_mysql_feedback(email,problem_description)
            st.success('您的信息已成功提交！')
            print(email)
            print(problem_description)