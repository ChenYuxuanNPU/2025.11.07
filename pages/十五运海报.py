from typing import Literal

import streamlit as st

st.set_page_config(
    page_icon="🏅",
    layout="wide",
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


display_centered_title(title=f"中华人民共和国第十五届运动会宣传海报", font_size=1)

l, m, r = st.columns(3)

with l:
    st.image("./static/十五运海报.png")

with m:
    st.image("./static/十五运海报.jpg")
    st.image("./static/十五运吉祥物.jpg")

with r:
    st.image("./static/十五运主题口号.jpg")
    st.image("./static/十五运会徽.jpg")
