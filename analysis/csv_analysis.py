import csv
from matplotlib import pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from pylab import *


name_index = 2
outdegree_index = 4

if __name__ == '__main__':
    rootCSV = open("../outputs/nodes_ipv6_2021_all.csv", "r", encoding='utf8')

    reader = csv.reader(rootCSV)

    limits = 12

    target = []
    names = []
    bottom = []

    i = 0
    for row in reader:
        # print(row[0], row[outdegree_index])
        target.append(row[0])
        if row[name_index] == '':
            if row[0] == '14840':  # 特别判断，部分AS名并没有被CAIDA识别
                names.append('BR Digital')
            else:
                names.append('')
        else:
            names.append(row[name_index])
        i += 1
        bottom.append([row[0], row[outdegree_index]])
        if i > limits:
            break
    target.pop(0)
    names.pop(0)
    bottom.pop(0)

    rootCSV.close()

    print(target)

    csv1 = open("../outputs/nodes_ipv6_2018_all.csv", "r", encoding='utf8')
    csv2 = open("../outputs/nodes_ipv6_2019_all.csv", "r", encoding='utf8')
    csv3 = open("../outputs/nodes_ipv6_2020_all.csv", "r", encoding='utf8')
    reader1 = csv.reader(csv1)
    reader2 = csv.reader(csv2)
    reader3 = csv.reader(csv3)

    values = []
    i = 0
    for asid in target:
        temp = []
        # print("当前id为：", asid)

        # 重置，回到文件顶部
        csv1.seek(0)
        csv2.seek(0)
        csv3.seek(0)

        flag = 0
        for row1 in reader1:
            if str(row1[0]) == asid:
                temp.append(int(row1[outdegree_index]))
                flag = 1
                break
        if flag == 0:
            temp.append(0)

        flag = 0
        for row2 in reader2:
            if str(row2[0]) == asid:
                temp.append(int(row2[outdegree_index]))
                flag = 1
                break
        if flag == 0:
            temp.append(0)

        flag = 0
        for row3 in reader3:
            # print(row3)
            if str(row3[0]) == asid:
                temp.append(int(row3[outdegree_index]))
                flag = 1
                break
        if flag == 0:
            temp.append(0)

        temp.append(int(bottom[i][1]))
        i += 1

        # print(temp)
        values.append(temp)
        # print()

    for i in range(limits):
        print(target[i], values[i])

    color_list = plt.cm.tab20(np.linspace(0, 1, 12))
    # # 在深色背景上绘制一系列线条时，可以在定性色图中选择一组离散的颜色
    # plt.cm.magma(np.linspace(0, 1, 15))

    # plt.rcParams['font.family'] = ['Times New Roman']
    mpl.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 单位是inches

    x = ['2018', '2019', '2020', '2021']

    for i in range(limits):
        plt.plot(x, values[i], color=color_list[i], marker='o', label=names[i] + ' (' + target[i] + ')')

    plt.legend(loc=9, ncol=3)  # 让图例生效
    # plt.xticks(x, names, rotation=1)
    # plt.margins(0)
    # plt.subplots_adjust(bottom=0.10)
    plt.xlabel('年份')  # X轴标签
    plt.ylabel("出度")  # Y轴标签
    plt.ylim(-300, 5500)  # Y轴区间

    # pyplot.yticks([0.70, 0.75, 0.80, 0.85, 0.90, 0.92])
    # pyplot.xticks([10, 20, 50, 100])

    # plt.title("A simple plot") #标题
    # plt.show()
    plt.savefig('/Users/yy/Desktop/2018-2021_outdegree.png')
