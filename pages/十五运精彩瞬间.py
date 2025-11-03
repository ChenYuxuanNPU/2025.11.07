from typing import Literal

import streamlit as st

st.set_page_config(
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="expanded"
)
def display_centered_title(title: str, font_size: Literal[1, 2, 3, 4, 5, 6]) -> None:
    """
    居中显示标题
    :param title: 标题内容
    :param font_size: 标题字体大小，1最大，2开始逐渐变小
    :return:
    """
    st.markdown(
        body=f"<h{font_size} style='text-align: center;'>{title}</h{font_size}>",
        unsafe_allow_html=True
    )


display_centered_title(title=f"十五运精彩瞬间", font_size=1)

st.image("./static/图片一.jpg")
st.image("./static/射击比赛.jpg")
st.image("./static/射击比赛2.jpg")
st.image("./static/气功比赛颁奖仪式.jpg")
st.image("./static/十五运彩排.jpg")