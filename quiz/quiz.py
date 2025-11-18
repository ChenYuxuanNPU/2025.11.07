import copy
import datetime
import string
import sys
import time
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from func import *

st.set_page_config(
    page_title="课堂练习",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "submitted_answer" not in st.session_state:
    st.session_state["submitted_answer"] = None

if "start_time" not in st.session_state:
    st.session_state["start_time"] = datetime.datetime.now()

end_time = None

quiz_content = read_xlsx_to_list(file_path=quiz_route)
quiz_result = read_json_to_dict(file_path=fr"{project_path}/quiz_result/result.json")

if quiz_title not in quiz_result.keys():
    quiz_result[quiz_title] = {"题目内容": 1}

quiz_info = {}

for num, item in enumerate(quiz_content[1:]):
    quiz_info[f"题目{num + 1}"] = {
        "题目内容": item[0],
        "题目选项": [option for option in item[2:] if option is not None],
        "答案": item[1]
    }

result = read_json_to_dict(file_path=fr"{project_path}/quiz_result/result.json")

#  这里要做一个简单的检查，判断json里有没有保存这次小测的内容，并尽可能快的更新，避免冲突
if quiz_title not in result.keys():
    result[quiz_title] = {
        "题目内容": {},
        "题目选项": {},
        "答案": {},
        "班级原始答案": {},
        "班级答题用时": {}
    }

    for num, item in enumerate(quiz_content[1:]):
        result[quiz_title]["题目内容"][f"题目{num + 1}"] = copy.deepcopy(quiz_info[f"题目{num + 1}"]["题目内容"])
        result[quiz_title]["题目选项"][f"题目{num + 1}"] = copy.deepcopy(quiz_info[f"题目{num + 1}"]["题目选项"])
        result[quiz_title]["答案"][f"题目{num + 1}"] = copy.deepcopy(quiz_info[f"题目{num + 1}"]["答案"])

    write_dict_to_json(result, file_path=fr"{project_path}/quiz_result/result.json")

#  如果这个result的json里没有某个班级的内容，就要赶紧先补充个插原始结果的字典，统计的事让quiz_result.py干
if class_name not in result[quiz_title]["班级原始答案"].keys():
    result[quiz_title]["班级原始答案"] = {
        class_name: {}
    }
    result[quiz_title]["班级答题用时"] = {
        class_name: []
    }

    write_dict_to_json(result, file_path=fr"{project_path}/quiz_result/result.json")

answer = [None] * (len(quiz_info.keys()) + 1)

_, mid, _ = st.columns(spec=[1, 3, 1])

with mid:
    display_centered_title(title=f"{quiz_title}", font_size=3)
    display_centered_title(title=f"课堂练习", font_size=4)

    answer[0] = st.number_input(
        "请输入你的学号：",
        max_value=60,
        min_value=1,
        value=None
    )

    for i, (key, value) in enumerate(quiz_info.items()):
        temp = {value["题目选项"][i]: string.ascii_uppercase[i] for i in range(len(value["题目选项"]))}
        temp[None] = None
        temp["None"] = None
        temp["ne"] = None  # 展示选项的时候默认返回值是空，所以切片后值为ne

        with st.container(border=True):
            if st.session_state["submitted_answer"]:
                if st.session_state["submitted_answer"][i] == list(result[quiz_title]["答案"].values())[i]:
                    st.success("回答正确！")
                else:
                    st.error(f'回答错误，正确答案为：{list(result[quiz_title]["答案"].values())[i]}')

            answer[i + 1] = temp[
                str(
                    st.radio(
                        f'**{i + 1}.{value["题目内容"]}**',
                        [fr"**{chara}.{item}**" for chara, item in
                         zip(list(string.ascii_uppercase[:len(value["题目选项"])]), value["题目选项"])],
                        index=None,
                        disabled=True if st.session_state["submitted_answer"] else False,
                    )
                ).replace("*", "")[2:]
            ]


    def submit_single_result():

        if None not in answer:
            if str(answer[0]) not in result[quiz_title]["班级原始答案"][class_name].keys():
                result[quiz_title]["班级原始答案"][class_name][answer[0]] = answer[1:]

                end_time = datetime.datetime.now()

                result[quiz_title]["班级答题用时"][class_name].append(
                    [answer[0], round((end_time - st.session_state["start_time"]).total_seconds(), 1)])

                write_dict_to_json(result, file_path=fr"{project_path}/quiz_result/result.json")

                while True:

                    temp_data = read_json_to_dict(file_path=fr"{project_path}/quiz_result/result.json")

                    if str(answer[0]) not in temp_data[quiz_title]["班级原始答案"][class_name].keys():
                        temp_data[quiz_title]["班级原始答案"][class_name][answer[0]] = answer[1:]
                        temp_data[quiz_title]["班级答题用时"][class_name].append(
                            [answer[0], round((end_time - st.session_state["start_time"]).total_seconds(), 1)])

                        write_dict_to_json(data=temp_data, file_path=fr"{project_path}/quiz_result/result.json")

                        time.sleep(1)

                    else:
                        break

                st.toast("提交成功！", icon="😋")
                st.balloons()

                st.session_state["submitted_answer"] = answer[1:]
            else:
                st.toast("只能提交一次喔！", icon="😇")

        elif answer[0] is None:
            st.toast("请填写学号！", icon="🥺")

        elif None in answer[1:]:
            unanswered_questions = []
            for i in range(len(answer)):
                if answer[i] is None:
                    unanswered_questions.append(i)
            st.toast(f"第{','.join(str(_) for _ in unanswered_questions)}题未回答！", icon="😯")


    _, mid_1, _ = st.columns([5.5, 1, 5.5])

    with mid_1:
        st.button("提交", on_click=submit_single_result,
                  disabled=True if st.session_state["submitted_answer"] else False, type="primary")
