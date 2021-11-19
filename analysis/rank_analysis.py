import csv
from matplotlib import pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np


name_index = 2
outdegree_index = 4


if __name__ == '__main__':
    rootCSV = open("../outputs/nodes_ipv6_2020_all.csv", "r", encoding='utf8')
    reader = csv.reader(rootCSV)

    limits = 12

    target = []
    names = []
    bottom = []

    i = 0
    for row in reader:

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

    csv1 = open("../outputs/nodes_ipv6_2021_all.csv", "r", encoding='utf8')
    reader1 = csv.reader(csv1)


    values = []

    ranks = []
    
    i = 0
    for i in range(len(target)):
        asid = target[i]
        tempOutdegree = []
        tempRank = []
        # print("当前id为：", asid)

        tempOutdegree.append(int(bottom[i][1]))
        tempRank.append(i+1)
        # 重置，回到文件顶部
        csv1.seek(0)

        flag = 0
        for index, row1 in enumerate(reader1):
            if str(row1[0]) == asid:
                tempOutdegree.append(int(row1[outdegree_index]))
                tempRank.append(index+1)
                flag = 1
                break
        if flag == 0:
            tempOutdegree.append(0)
        i +=1
        values.append(tempOutdegree)
        ranks.append(tempRank)

    for i in range(limits):
        print(names[i], target[i], values[i])

    print()

    for i in range(limits):
        print(names[i], target[i], ranks[i])



    color_list = plt.cm.tab20(np.linspace(0, 1, 12))
    # # 在深色背景上绘制一系列线条时，可以在定性色图中选择一组离散的颜色
    # plt.cm.magma(np.linspace(0, 1, 15))

    plt.rcParams['font.family'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['figure.figsize'] = (10, 7.0) # 单位是inches

    x = ['2020', '2021']

    for i in range(limits):
        plt.plot(x, values[i], color=color_list[i], marker='o', label=names[i]+' ('+target[i]+')')

    # for i in range(limits):
    #     if i == 9:
    #         continue
    #     plt.plot(x, ranks[i], color=color_list[i], marker='o', label=names[i]+' ('+target[i]+')')

    plt.legend(loc=9, ncol=3)  # 让图例生效
    # plt.xticks(x, names, rotation=1)
    # plt.margins(0)
    # plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Year')  # X轴标签
    plt.ylabel("Outdegree")  # Y轴标签
    # plt.ylabel("Rank")  # Y轴标签
    plt.ylim(-300, 5500)  # Y轴区间
    # plt.ylim(0, 30)  # Y轴区间

    plt.show()





