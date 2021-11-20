import csv
from matplotlib import pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from pylab import *

name_index = 2
outdegree_index = 4

temp_list1 = [1, 1000, 2000, 4000, 8000]
temp_list2 = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

def draw_suffix_graph(v4_outdegrees, v6_outdegrees):
    v4_outdegrees = sorted(v4_outdegrees)
    v6_outdegrees = sorted(v6_outdegrees)
    # 后缀和
    # 举例：suffix_num1[i] 就是 >= suffix_list [i] 的 v4 AS的数量
    '''
        后缀和的一种方法是 总数-前缀和，但这个前缀和不能加等号，而是严格小于
    '''
    suffix_list = temp_list2

    suffix_num1 = []
    suffix_num2 = []

    index1 = 0
    index2 = 0
    for i in range(len(suffix_list)):
        if i == 0:
            base1 = 0
            base2 = 0
        else:
            base1 = suffix_num1[i - 1]
            base2 = suffix_num2[i - 1]
        # 假设此时 index1 表示在v4_outdegrees的下标
        while index1 < len(v4_outdegrees):  # 防止越界
            if int(v4_outdegrees[index1]) < suffix_list[i]:
                base1 += 1
                index1 += 1  # 移动到下一个
            else:  # 不满足条件了，跳出
                break

        while index2 < len(v6_outdegrees):  # 防止越界
            if int(v6_outdegrees[index2]) < suffix_list[i]:
                base2 += 1
                index2 += 1  # 移动到下一个
            else:  # 不满足条件了，跳出
                break
        suffix_num1.append(base1)
        suffix_num2.append(base2)

    for i in range(len(suffix_num1)):
        suffix_num1[i] = len(v4_outdegrees) - suffix_num1[i]
    for i in range(len(suffix_num2)):
        suffix_num2[i] = len(v6_outdegrees) - suffix_num2[i]

    print(suffix_num1)
    print(suffix_num2)

    for i in range(len(suffix_list)):
        suffix_list[i] = '≥'+str(suffix_list[i])

    color_list = plt.cm.Set1(np.linspace(0, 1, 9))
    # # 在深色背景上绘制一系列线条时，可以在定性色图中选择一组离散的颜色
    # plt.rcParams['font.family'] = ['Times New Roman']
    mpl.rcParams['font.sans-serif'] = ['SimSun']

    plt.rcParams.update({'font.size': 10})
    plt.rcParams['figure.figsize'] = (14.0, 8.0)  # 单位是inches

    plt.plot(suffix_list, suffix_num1, color=color_list[0], marker='o', label="IPv4")
    plt.plot(suffix_list, suffix_num2, color=color_list[1], marker='o', label="IPv6")

    plt.legend(loc=9, ncol=2)  # 让图例生效
    plt.xlabel('出度')  # X轴标签
    plt.ylabel("AS数量")  # Y轴标签
    # plt.ylim(0, 500)  # Y轴区间

    # 图注释（点的坐标）
    # zip joins x and y coordinates in pairs
    for x, y in zip(suffix_list, suffix_num1):
        label = "{:d}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    # zip joins x and y coordinates in pairs
    for x, y in zip(suffix_list, suffix_num2):
        label = "{:d}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    # plt.show()
    plt.savefig('/Users/yy/Desktop/suffix_v4_v6.png')
    clf()  # 清图。
    cla()  # 清坐标轴。
    close()  # 关窗口


if __name__ == '__main__':

    limits = 1e10

    # IPv4
    v4_CSV = open("../outputs/nodes_ipv4_2021_all.csv", "r", encoding='utf8')
    reader1 = csv.reader(v4_CSV)
    v4_ids = []
    v4_names = []
    v4_outdegrees = []

    i = 0
    for row in reader1:
        if i == 0:  # 跳过第一行表头
            i += 1
            continue

        if i > limits:
            break

        v4_ids.append(row[0])
        v4_names.append(row[name_index])
        v4_outdegrees.append(int(row[outdegree_index]))
        i += 1


    v4_CSV.close()

    print(v4_outdegrees)

    # for i in range(len(v4_ids)):
    #     print(i, v4_names[i], v4_outdegrees[i])


    # IPv6
    v6_CSV = open("../outputs/nodes_ipv6_2021_all.csv", "r", encoding='utf8')
    reader2 = csv.reader(v6_CSV)
    v6_ids = []
    v6_names = []
    v6_outdegrees = []

    i = 0
    for row in reader2:
        if i == 0:  # 跳过第一行表头
            i += 1
            continue

        if i > limits:
            break

        v6_ids.append(row[0])
        v6_names.append(row[name_index])
        v6_outdegrees.append(int(row[outdegree_index]))
        i += 1


    v6_ids.pop(0)
    v6_names.pop(0)
    v6_outdegrees.pop(0)
    v6_CSV.close()

    print(v6_outdegrees)

    draw_suffix_graph(v4_outdegrees, v6_outdegrees)






