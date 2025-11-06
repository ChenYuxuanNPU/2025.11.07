from datetime import datetime, time

from func import *

st.set_page_config(
    page_title="第十五届全运会资源中心",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主标题样式 */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #e0e0e0;
    }

    /* 信息卡片样式 */
    .info-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1890ff;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* 提示框样式 */
    .tip-box {
        background-color: #e6f7ff;
        border: 1px solid #91d5ff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }

    /* 按钮样式 */
    .stButton button {
        background: linear-gradient(45deg, #1890ff, #096dd9);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    /* 页脚样式 */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)


# 主页面内容
def main():
    # 主标题区域
    st.markdown("""
    <div class="main-title">
        <h1>🏅 中华人民共和国第十五届运动会</h1>
        <h3>在线资源中心</h3>
    </div>
    """, unsafe_allow_html=True)

    # 使用列布局创建更现代的布局
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # 欢迎信息卡片
        st.markdown("""
        <div class="info-card">
            <h4>🎯 欢迎使用全运会资源平台</h4>
            <p>这里汇集了第十五届全运会的各类资源文件，包括文档、图片、视频等多媒体资料。</p>
        </div>
        """, unsafe_allow_html=True)

        # 操作指南区域
        st.markdown("""
        <div class="tip-box">
            <h4>📋 使用指南</h4>
        </div>
        """, unsafe_allow_html=True)

        # 使用列布局显示操作步骤
        step_col1, step_col2 = st.columns(2)

        with step_col1:
            st.info("""
            **📝 文字复制**
            1. 选中需要复制的文字
            2. 右键点击选择"复制"
            3. 或使用快捷键 Ctrl+C
            """)

        with step_col2:
            st.info("""
            **🖼️ 图片下载**
            1. 在图片上右键单击
            2. 选择"图片另存为"
            3. 选择保存位置即可
            """)

    # 页脚
    st.markdown("""
    <div class="footer">
        <p>© 2025 广州市白云区教育研究院</p>
        <p>建议使用 Chrome、Firefox 等现代浏览器访问以获得最佳体验</p>
    </div>
    """, unsafe_allow_html=True)

    if datetime.now().time() >= time(int(quiz_start_time.split(":")[0]), int(quiz_start_time.split(":")[1])):
        st.markdown(
            """
            <div style="text-align: center;">
                <a href="http://192.168.31.201:8502/" target="_blank" style="
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px;
                ">跳转到课堂小测</a>
            </div>
            """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    # 初始化session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

    main()
