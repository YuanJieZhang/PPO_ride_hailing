import numpy as np
import csv
from numpy.random import default_rng

def process_csv_data(file_path):
    # 使用numpy的默认随机数生成器
    rng = default_rng()

    # 读取CSV文件
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data_list = list(reader)

    # 处理数据只保留前四列, 并转换坐标
    processed_data = []
    for row in data_list:
        # 去掉坐标中的字母部分，只保留数字
        start_coord = int(''.join(filter(str.isdigit, row[0])))
        end_coord = int(''.join(filter(str.isdigit, row[3])))
        distance = float(row[2])
        processed_data.append([start_coord, end_coord, distance])

    # 生成时间点, 分布为18个1, 18个2, 和19个3
    time_points = np.hstack((np.ones(18, dtype=int) * 1,
                             np.ones(18, dtype=int) * 2,
                             np.ones(19, dtype=int) * 3))

    # 确保生成的时间点被随机分布
    rng.shuffle(time_points)

    # 将时间点追加到processed_data的每一行中
    for i in range(len(processed_data)):
        processed_data[i].append(time_points[i])

    # 转换为numpy structured array

    return processed_data

# 使用方法
structured_data = process_csv_data('bay_vio_data_03_19.csv')

# 输出以确认结果
print(structured_data)