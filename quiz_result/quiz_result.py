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
    page_title="课堂练习情况",
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

if quiz_name and current_class and len(data["班级原始答案"][current_class].keys()) > 0:
    standard_answer = data["答案"].values()
    student_answers = list(data["班级原始答案"][current_class].values())

    with st.container(border=True):
        display_centered_title(title=f'总体完成情况', font_size=2)

        st.divider()

        l, r = st.columns([2, 1])

        with l:
            draw_bar_chart(
                data=calculate_total_scores(std_ans=list(standard_answer), stu_ans=list(student_answers)),
                title="总体得分情况"
            )

            draw_bar_chart(
                data=calculate_discrete_total_scores(std_ans=list(standard_answer), stu_ans=list(student_answers)),
                title="各题正确人数"
            )
        with r:
            st.info("得分情况前十五排名")
            st.divider()

            # 计算所有学生的学号和成绩，按成绩降序排列
            list_2 = sorted(
                [[key, calculate_score(list_std=list(standard_answer), list_stu=value)] for key, value in
                 raw_data[quiz_name]["班级原始答案"][class_name].items()], key=lambda x: x[1], reverse=True)
            # 获取dataframe的左列序号列
            list_1 = [i for i in range(1, len(list_2) + 1)]
            list_3 = []

            # list_3用来保存每个学生的答题用时，一维列表
            for item in list_2:
                stu_id = item[0]
                for item_1 in data.get("班级答题用时",{}).get(class_name,{}):
                    if str(item_1[0]) == str(stu_id):
                        list_3.append(item_1[1])

            list_for_df = []

            for i in range(len(list_1)):
                list_for_df.append(list_2[i])
                list_for_df[-1].append(list_3[i])

            list_for_df = sorted(list_for_df, key=lambda x: (-x[1], x[2]))
            list_for_df = [[one_item] + two_item for one_item, two_item in zip(list_1, list_for_df)]

            st.dataframe(
                data=pd.DataFrame(
                    data=list_for_df[:15],
                    columns=['排名', '学生学号', '练习得分', '答题用时']
                ),
                hide_index=True,
                height=650
            )

        # with r2:
        #     st.info("完成速度前十五排名")
        #     st.divider()
        #
        #     st.dataframe(
        #         data=pd.DataFrame(
        #             data=sorted(raw_data[quiz_name]["班级答题用时"][class_name], key=lambda x: x[1])[:15],
        #             columns=['学生学号', '答题用时'],
        #         ),
        #         hide_index=False,
        #         height=650
        #     )

    st.divider()

    with st.container(border=True):
        display_centered_title(title=f'各题完成情况', font_size=2)

        for i in range(1, len(standard_answer) + 1):
            with st.container(border=True):
                display_centered_title(title=f'第{i}题完成情况', font_size=3)

                l, r = st.columns(spec=2)

                with l:

                    draw_bar_chart(
                        data=convert_to_frequency_dict(letter_list=[item[i - 1] for item in list(value for value in
                                                                                                 raw_data.get(
                                                                                                     quiz_title,
                                                                                                     {}).get(
                                                                                                     "班级原始答案",
                                                                                                     {}).get(class_name,
                                                                                                             {}).values())],
                                                       max_letter=chr(
                                                           64 + len(
                                                               raw_data.get(quiz_title, {}).get("题目选项", {}).get(
                                                                   f"题目{i}", {})))),
                        title=f"第{i}题得分情况"
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

                    elif accuracy > 25:
                        st.warning(
                            f'本题正确率为：{accuracy}%，正确答案为：{raw_data.get(quiz_title, {}).get("答案", {}).get(f"题目{i}", None)}')

                    else:
                        st.error(
                            f'本题正确率为：{accuracy}%，正确答案为：{raw_data.get(quiz_title, {}).get("答案", {}).get(f"题目{i}", None)}')

                    st.radio(
                        f'**{i}.{raw_data.get(quiz_title, {}).get("题目内容", {}).get(f"题目{i}", "")}**',
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
