import csv
from matplotlib import pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from pylab import *

name_index = 2
outdegree_index = 4

temp_list1 = [1, 1000, 2000, 4000, 8000]
temp_list2 = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

def draw_prefix_graph(CN_outdegrees, US_outdegrees):
    CN_outdegrees = sorted(CN_outdegrees)
    US_outdegrees = sorted(US_outdegrees)
    # 前缀和
    prefix_list = temp_list1
    # 举例：prefix_num1[i] 就是 <= prefix_list [i] 的 CN AS的数量
    prefix_num1 = []
    prefix_num2 = []

    index1 = 0
    index2 = 0
    for i in range(len(prefix_list)):
        if i == 0:
            base1 = 0
            base2 = 0
        else:
            base1 = prefix_num1[i - 1]
            base2 = prefix_num2[i - 1]
        # 假设此时 index1 表示在CN_outdegrees的下标
        while index1 < len(CN_outdegrees):  # 防止越界
            if CN_outdegrees[index1] <= prefix_list[i]:
                base1 += 1
                index1 += 1  # 移动到下一个
            else:  # 不满足条件了，跳出
                break

        while index2 < len(US_outdegrees):  # 防止越界
            if US_outdegrees[index2] <= prefix_list[i]:
                base2 += 1
                index2 += 1  # 移动到下一个
            else:  # 不满足条件了，跳出
                break
        prefix_num1.append(base1)
        prefix_num2.append(base2)

    print(prefix_num1)
    print(prefix_num2)

    # 转成字符串作为横坐标
    for i in range(len(prefix_list)):
        prefix_list[i] = '≤'+str(prefix_list[i])

    color_list = plt.cm.Set1(np.linspace(0, 1, 9))
    # # 在深色背景上绘制一系列线条时，可以在定性色图中选择一组离散的颜色
    # plt.rcParams['font.family'] = ['Times New Roman']
    mpl.rcParams['font.sans-serif'] = ['SimSun']

    plt.rcParams.update({'font.size': 10})
    plt.rcParams['figure.figsize'] = (9.0, 6.0)  # 单位是inches

    plt.plot(prefix_list, prefix_num1, color=color_list[0], marker='o', label="中国")
    plt.plot(prefix_list, prefix_num2, color=color_list[1], marker='o', label="美国")

    plt.legend(loc=9, ncol=2)  # 让图例生效
    plt.xlabel('出度')  # X轴标签
    plt.ylabel("AS数量")  # Y轴标签
    plt.ylim(0, 500)  # Y轴区间

    # 图注释（点的坐标）
    # zip joins x and y coordinates in pairs
    for x, y in zip(prefix_list, prefix_num1):
        label = "{:d}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    # zip joins x and y coordinates in pairs
    for x, y in zip(prefix_list, prefix_num2):
        label = "{:d}".format(y)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    # plt.title("A simple plot") #标题

    plt.show()
    # plt.savefig('/Users/yy/Desktop/prefix_CN_US.png')
    # clf()  # 清图。
    # cla()  # 清坐标轴。
    # close()  # 关窗口


def draw_suffix_graph(CN_outdegrees, US_outdegrees):
    CN_outdegrees = sorted(CN_outdegrees)
    US_outdegrees = sorted(US_outdegrees)

    # 后缀和
    # 举例：suffix_num1[i] 就是 >= suffix_list [i] 的 CN AS的数量
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
        # 假设此时 index1 表示在CN_outdegrees的下标
        while index1 < len(CN_outdegrees):  # 防止越界
            if CN_outdegrees[index1] < suffix_list[i]:
                base1 += 1
                index1 += 1  # 移动到下一个
            else:  # 不满足条件了，跳出
                break

        while index2 < len(US_outdegrees):  # 防止越界
            if US_outdegrees[index2] < suffix_list[i]:
                base2 += 1
                index2 += 1  # 移动到下一个
            else:  # 不满足条件了，跳出
                break
        suffix_num1.append(base1)
        suffix_num2.append(base2)

    for i in range(len(suffix_num1)):
        suffix_num1[i] = len(CN_outdegrees) - suffix_num1[i]
    for i in range(len(suffix_num2)):
        suffix_num2[i] = len(US_outdegrees) - suffix_num2[i]

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

    plt.plot(suffix_list, suffix_num1, color=color_list[0], marker='o', label="中国")
    plt.plot(suffix_list, suffix_num2, color=color_list[1], marker='o', label="美国")

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

    # plt.title("A simple plot") #标题
    # plt.show()
    plt.savefig('/Users/yy/Desktop/suffix_CN_US.png')
    clf()  # 清图。
    cla()  # 清坐标轴。
    close()  # 关窗口


if __name__ == '__main__':

    limits = 1e10

    # 中国
    CN_CSV = open("../outputs_CN_US/nodes_ipv4&6_2021_CN.csv", "r", encoding='utf8')
    reader1 = csv.reader(CN_CSV)
    CN_ids = []
    CN_names = []
    CN_outdegrees = []

    i = 0
    for row in reader1:
        if i == 0:  # 跳过第一行表头
            i += 1
            continue

        if i > limits:
            break

        CN_ids.append(row[0])
        CN_names.append(row[name_index])
        CN_outdegrees.append(int(row[outdegree_index]))
        i += 1


    CN_CSV.close()

    # for i in range(len(CN_ids)):
    #     print(i, CN_names[i], CN_outdegrees[i])


    # 美国
    US_CSV = open("../outputs_CN_US/nodes_ipv4&6_2021_US.csv", "r", encoding='utf8')
    reader2 = csv.reader(US_CSV)
    US_ids = []
    US_names = []
    US_outdegrees = []

    i = 0
    for row in reader2:
        if i == 0:  # 跳过第一行表头
            i += 1
            continue

        if i > limits:
            break

        US_ids.append(row[0])
        US_names.append(row[name_index])
        US_outdegrees.append(int(row[outdegree_index]))
        i += 1


    US_ids.pop(0)
    US_names.pop(0)
    US_outdegrees.pop(0)
    US_CSV.close()

    # draw_prefix_graph(CN_outdegrees, US_outdegrees)
    draw_suffix_graph(CN_outdegrees, US_outdegrees)






