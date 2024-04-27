import csv
import numpy as np

def process_csv_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data_list = list(reader)

    # 跳过标题行
    data_list = data_list[1:]

    # 处理数据，分割点坐标，并保留距离
    processed_data = []
    for row in data_list:
        # 分割起始点坐标（假定坐标间始终是用"_"分隔的）
        start_point, end_point = row[1].split('_')
        # 去掉字母部分，保留数字
        start_num = int(''.join(filter(str.isdigit, start_point)))
        end_num = int(''.join(filter(str.isdigit, end_point)))
        distance = int(row[0])
        # 将处理后的结果作为列表添加到processed_data中
        processed_data.append([start_num, end_num, distance])

    # 转换为NumPy数组

    return processed_data

# 使用方法
structured_data = process_csv_data('dis_CBD_twoPs_03_19.csv')

# 输出以确认结果
print(structured_data)