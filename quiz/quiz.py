import re
import uuid

import openpyxl
import streamlit as st

quiz_route = r"C:\Users\10129\Desktop\python\streamlit_test\quiz\课后习题.xlsx"
quiz_title = fr"七年级第三单元第二节——网站开发前的准备"


#  ""

st.set_page_config(
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def remove_zero_width_chars(text):
    # 移除所有零宽字符（包括\u200c, \u200d, \u200e, \u200f, \uFEFF等）
    return re.sub(r'[\u200c\u200d\u200e\u200f\uFEFF]', '', text)

def read_xlsx_to_list(file_path, sheet_name=None):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active if sheet_name is None else workbook[sheet_name]

    data = []
    for row in sheet.iter_rows(values_only=True):
        processed_row = []
        for cell_value in row:
            if isinstance(cell_value, str):
                cell_value = remove_zero_width_chars(cell_value).strip()
            processed_row.append(cell_value)
        data.append(processed_row)

    return data


def extract_number(text):
    """
    从字符串中提取数字

    Args:
        text (str): 包含数字的字符串，如"题目1"

    Returns:
        int: 提取到的数字，如果未找到数字返回None
    """
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

data = read_xlsx_to_list(file_path=quiz_route)

statistics = {}

print(data)

for num,item in enumerate(data[1:]):
    statistics[f"题目{num+1}"] = {
        "题目内容":item[0],
        "题目选项":[option for option in item[2:] if option is not None],
        "答案":item[1],
        "学生答案":{}
    }

answer = [None] * (len(statistics.keys()) +1)

answer[0] = st.number_input(
    "学号",
    max_value=55,
    min_value=1,
    value=None
)

for i, (key, value) in enumerate(statistics.items()):
    answer[i+1] = st.radio(
        f'{i+1}.{value["题目内容"]}',
        [item for item in value["题目选项"]],
        index=None,
    )

    st.divider()

st.button("提交")
st.write(answer)
