import copy
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
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
        "统计结果": {}  # todo:要删
    }

    for num, item in enumerate(quiz_content[1:]):
        result[quiz_title]["题目内容"][f"题目{num + 1}"] = copy.deepcopy(quiz_info[f"题目{num + 1}"]["题目内容"])
        result[quiz_title]["题目选项"][f"题目{num + 1}"] = copy.deepcopy(quiz_info[f"题目{num + 1}"]["题目选项"])
        result[quiz_title]["答案"][f"题目{num + 1}"] = copy.deepcopy(quiz_info[f"题目{num + 1}"]["答案"])
        result[quiz_title]["统计结果"][f'题目{num + 1}（{result[quiz_title]["答案"][f"题目{num + 1}"]}）'] = {c: 0 for c
                                                                                                            in
                                                                                                            ["A", "B",
                                                                                                             "C",
                                                                                                             "D"]}  # todo:记得后面改的时候要删

    write_dict_to_json(result, file_path=fr"{project_path}/quiz_result/result.json")

#  如果这个result的json里没有某个班级的内容，就要赶紧先补充个插原始结果的字典，统计的事让quiz_result.py干
if class_name not in result[quiz_title].keys():
    result[quiz_title][class_name] = {
        "学生原始答案": {},
    }

    write_dict_to_json(result, file_path=fr"{project_path}/quiz_result/result.json")

answer = [None] * (len(quiz_info.keys()) + 1)

display_centered_title(title=f"{quiz_title}", font_size=3)
display_centered_title(title=f"课后习题", font_size=4)

answer[0] = st.number_input(
    "请输入你的学号：",
    max_value=55,
    min_value=1,
    value=None
)

for i, (key, value) in enumerate(quiz_info.items()):
    temp = {value["题目选项"][i]: string.ascii_uppercase[i] for i in range(len(value["题目选项"]))}
    temp[None] = None
    st.divider()

    answer[i + 1] = temp[
        st.radio(
            f'**{i + 1}.{value["题目内容"]}**',
            [item for item in value["题目选项"]],
            index=None,
        )]


def submit_single_result():
    if None not in answer:
        if str(answer[0]) not in result[quiz_title][class_name]["学生原始答案"].keys():
            result[quiz_title][class_name]["学生原始答案"][answer[0]] = answer[1:]

            for i in range(1, len(answer)):
                result[quiz_title]["统计结果"][f'题目{i}（{result[quiz_title]["答案"][f"题目{i}"]}）'][answer[i]] += 1
            write_dict_to_json(result, file_path=fr"{project_path}/quiz_result/result.json")
            st.toast("提交成功！", icon="😋")
        else:
            st.toast("只能提交一次喔！", icon="😇")

    elif answer[0] is None:
        st.toast("请填写学号！", icon="🥺")

    elif None in answer[1:]:
        unanswered_questions = []
        for i in range(len(answer)):
            if answer[i] is None:
                unanswered_questions.append(i)
        st.toast(f'第{"，".join(str(_) for _ in unanswered_questions)}题未回答！', icon="😯")


st.button("提交", on_click=submit_single_result)

st.write(answer)
