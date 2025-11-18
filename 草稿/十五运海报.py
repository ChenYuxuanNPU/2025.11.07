import sys
from pathlib import Path
from typing import Literal

import streamlit as st

st.set_page_config(
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from func import *


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
st.divider()


with st.container(border=True):
    l, m, r = st.columns(3)

    with l:
        st.image(f"{project_path}/pic/十五运海报.png")

    with m:
        st.image(f"{project_path}/pic/十五运吉祥物.jpg")
        st.image(f"{project_path}/pic/十五运海报.jpg")

    with r:
        st.image(f"{project_path}/pic/十五运主题口号.jpg")
        st.image(f"{project_path}/pic/十五运会徽.jpg")
