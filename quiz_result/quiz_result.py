import string
import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from func import *

st.set_page_config(
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

raw_data = read_json_to_dict(file_path=f'{project_path}/quiz_result/result.json')

display_centered_title(title=f'课堂训练统计结果', font_size=1)
st.divider()

l, r = st.columns(spec=2)
with l:
    quiz_name = st.selectbox(
        label="请选择训练内容",
        placeholder="训练章节",
        options=raw_data.keys(),
        index=None
    )
with r:
    current_class = st.selectbox(
        label="请选择班级",
        placeholder="班级",
        options=[item for item in raw_data.get(quiz_name, {}).get("班级原始答案", {}).keys()],
        disabled=not quiz_name,
        index=None
    )
st.divider()

data = raw_data.get(quiz_name, None)

if quiz_name and current_class:
    standard_answer = data["答案"].values()
    student_answers = list(data["班级原始答案"][current_class].values())

    with st.container(border=True):
        display_centered_title(title=f'总体完成情况', font_size=2)

        st.divider()

        l, r1, r2 = st.columns([2, 1, 1])

        with l:
            draw_bar_chart(
                data=calculate_total_scores(std_ans=list(standard_answer), stu_ans=list(student_answers)),
                title="得分情况"
            )

            draw_bar_chart(
                data=calculate_discrete_total_scores(std_ans=list(standard_answer), stu_ans=list(student_answers)),
                title="各题正确人数"
            )
        with r1:
            st.info("得分情况前十五排名")
            st.divider()

            st.dataframe(
                data=pd.DataFrame(
                    data=sorted(
                        [[key, calculate_score(list_std=list(standard_answer), list_stu=value)] for key, value in
                         raw_data[quiz_name]["班级原始答案"][class_name].items()], key=lambda x: x[1], reverse=True)[
                         :15],
                    columns=['学生学号', '练习结果']
                ),
                hide_index=False,
                height=650
            )

        with r2:
            st.info("完成速度前十五排名")
            st.divider()

            st.dataframe(
                data=pd.DataFrame(
                    data=sorted(raw_data[quiz_name]["班级答题用时"][class_name], key=lambda x: x[1])[:15],
                    columns=['学生学号', '答题用时'],
                ),
                hide_index=False,
                height=650
            )

    st.divider()

    with st.container(border=True):
        display_centered_title(title=f'各题完成情况', font_size=2)

        for i in range(1, len(standard_answer) + 1):
            with st.container(border=True):
                display_centered_title(title=f'第{i}题完成情况', font_size=3)

                l, r = st.columns(spec=2)

                with l:

                    draw_bar_chart(
                        data=convert_to_frequency_dict([item[i - 1] for item in list(value for value in
                                                                                     raw_data.get(quiz_title, {}).get(
                                                                                         "班级原始答案", {}).get(
                                                                                         class_name, {}).values())]),
                        title="本题得分情况"
                    )

                with r:

                    accuracy = round(100 * sum(
                        item == raw_data.get(quiz_title, {}).get("答案", {}).get(f"题目{i}", None) for item in
                        [item[i - 1] for item in list(value for value in
                                                      raw_data.get(quiz_title, {}).get("班级原始答案", {}).get(
                                                          class_name, {}).values())]) / len([item[i - 1] for item in
                                                                                             list(value for value in
                                                                                                  raw_data.get(
                                                                                                      quiz_title,
                                                                                                      {}).get(
                                                                                                      "班级原始答案",
                                                                                                      {}).get(
                                                                                                      class_name,
                                                                                                      {}).values())]),
                                     1)

                    if accuracy > 80:
                        st.success(
                            f'本题正确率为：{accuracy}%，正确答案为：{raw_data.get(quiz_title, {}).get("答案", {}).get(f"题目{i}", None)}')

                    elif accuracy > 60:
                        st.info(
                            f'本题正确率为：{accuracy}%，正确答案为：{raw_data.get(quiz_title, {}).get("答案", {}).get(f"题目{i}", None)}')

                    else:
                        st.warning(
                            f'本题正确率为：{accuracy}%，正确答案为：{raw_data.get(quiz_title, {}).get("答案", {}).get(f"题目{i}", None)}')

                    st.radio(
                        f'**{i}.{raw_data.get(quiz_title, {}).get("题目内容", {}).get(f'题目{i}', "")}**',
                        [fr"**{chara}.{item}**" for chara, item in
                         zip(list(string.ascii_uppercase[:len([f"**{items}**" for items in
                                                               raw_data.get(quiz_title, {}).get("题目选项", {}).get(
                                                                   f'题目{i}', "")])]), [f"**{items}**" for items in
                                                                                         raw_data.get(quiz_title,
                                                                                                      {}).get(
                                                                                             "题目选项", {}).get(
                                                                                             f'题目{i}', "")])],
                        # [f"**{items}**" for items in raw_data.get(quiz_title, {}).get("题目选项", {}).get(f'题目{i - 1}', "")],
                        index=None,
                    )
