import streamlit as st



pages = {
    "开始体验": [
        st.Page("detection.py", title="设备选择"),
        st.Page("dynamic_detect.py", title="实时检测"),
        st.Page("report.py", title="检测结果"),
        st.Page("expert.py", title="ChatGLM智能建议"),
    ],
    "检测记录": [
        st.Page("history_db.py", title="我的检测"),
    ],
    "技术支持": [
        st.Page("skills.py", title="技术社区"),
    ],
    "联系我们": [
        st.Page("contract.py", title="联系我们"),
    ],
}

pg = st.navigation(pages)
pg.run()

st.logo("tyut.png",size="large")
st.sidebar.markdown("物联网2201 :open_hands:")
st.sidebar.markdown("特别鸣谢|指导老师|:woman:")
st.sidebar.markdown("实习时间:24.12.23-24.1.3")
