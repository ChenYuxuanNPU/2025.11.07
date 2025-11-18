import json
import os
import re
from collections import Counter
from typing import Literal

import openpyxl
import pandas as pd
import pyecharts.options as opts
import streamlit as st
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

project_path = os.path.dirname(os.path.abspath(__file__))

quiz_start_time = "8:20"  # 11.15
class_name = "七年10班"
quiz_route = fr"{project_path}\quiz\七年级第三单元第二节——网站开发前的准备.xlsx"

quiz_title = os.path.splitext(os.path.basename(quiz_route))[0]


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


def calculate_score(list_std: list, list_stu: list) -> int:
    """
    用于计算每个学生答案的成绩
    :param list_std: 标准答案，字符串列表
    :param list_stu: 某一个学生答案，字符串列表
    :return:
    """

    return sum(a == b for a, b in zip(list_std, list_stu)) if len(list_std) == len(list_stu) else 0


def calculate_total_scores(std_ans: list | set, stu_ans: list[list]) -> list[list]:
    """
    获取标准答案列表和学生作答列表，返回一个字典
    :param std_ans: 标准答案，字符串列表
    :param stu_ans: 学生答案，键为成绩，值为人数
    :return:
    """

    temp = []

    for item in stu_ans:
        temp.append(calculate_score(list_std=std_ans, list_stu=item))

    output = {num: 0 for num in range(len(std_ans) + 1)}

    for item in temp:
        output[item] += 1

    return output


def draw_bar_chart(data: pd.DataFrame | dict, title: str, height: int = 0, axis_font_size: int = 12, ) -> None:
    """
    绘制柱状图
    :param data: 绘图所用数据
    :param title: 图表标题
    :param height: 图表高度，默认根据分辨率自适应
    :param axis_font_size: 坐标轴标签字体大小
    :return:
    """

    if isinstance(data, dict):
        chart = Bar()
        chart.add_xaxis([keys for keys in data.keys()])
        chart.add_yaxis("总人数", [values for values in data.values()])

    elif isinstance(data, pd.DataFrame):
        return None

    else:
        return None

    chart.set_global_opts(title_opts=opts.TitleOpts(title=title),
                          legend_opts=opts.LegendOpts(is_show=False),
                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=axis_font_size)),
                          yaxis_opts=opts.AxisOpts(
                              max_=((max(list(data.values())) + 4) // 5) * 5,
                              interval=((max(list(data.values())) + 4) // 5)
                          ),
                          )

    chart.set_series_opts(label_opts=opts.LabelOpts(position="top", is_show=False))

    st_pyecharts(
        chart=chart,
        height=f"400px"
    )

    return None


def calculate_discrete_total_scores(std_ans: list | set, stu_ans: list[list]) -> dict:
    """
    获取标准答案列表和学生作答列表，返回一个字典
    :param std_ans: 标准答案，字符串列表
    :param stu_ans: 学生答案，二维字符串列表
    :return: 字典，键为题号，值为人数
    """
    output = {f'第{key}题': 0 for key in range(1, len(std_ans) + 1)}

    for i in range(1, len(std_ans) + 1):
        for ans in stu_ans:

            if ans[i - 1] == list(std_ans)[i - 1]:
                output[f"第{i}题"] += 1

    return output


def convert_to_frequency_dict(letter_list: list, max_letter: str = None) -> dict:
    """
    将大写字母列表转换为带顺序的字典，且补全中间缺漏的大写字母
    :param letter_list: 原大写字母列表
    :param max_letter: 最大的选项序号
    :return: 频数字典，键为字母，值为频数
    """
    if not letter_list:  # 处理空列表情况
        return {}

    # 找到列表中最大的字母
    if max_letter is None:
        max_letter = max(letter_list)

    # 统计频数
    counter = Counter(letter_list)

    # 生成从A到最大字母的字典
    result = {}
    for ascii_code in range(65, ord(max_letter) + 1):
        letter = chr(ascii_code)
        result[letter] = counter.get(letter, 0)

    return result


if __name__ == '__main__':
    print(quiz_title)
