import json
import os
import re
from typing import Literal

import openpyxl
import streamlit as st

quiz_title = fr"七年级第三单元第二节——网站开发前的准备"
quiz_start_time = "11:08"
class_name = "七年12班"

project_path = os.path.dirname(os.path.abspath(__file__))
quiz_route = fr"{project_path}\quiz\课后习题.xlsx"


def read_json_to_dict(file_path: str):
    """读取JSON文件为字典"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_dict_to_json(data: dict, file_path: str):
    """将字典写入JSON文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


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
