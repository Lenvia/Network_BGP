import csv
from collections import defaultdict

mode = 'ipv4&6'
year = '2021'
area_list = ['CN', 'US', 'CN&US']  # 地区
area = area_list[1]

org_asn = defaultdict(list)  # 组织所管辖的AS列表
asn_org = defaultdict(str)  # AS编号到组织的映射
org_country = defaultdict(str)  # 组织到国家/地区的映射
asn_name = defaultdict(str)

buffer = defaultdict(str)  # (as1, as2) -> ipv4/ipv6/ipv4&6


# 读取asn_org文件，并将asn, org_id, country 的关系提取并放入上面几个集合里
def dealCountry(asn_org_file):
    format_counter = 0
    with open(asn_org_file) as f:
        for line in f:
            if line.startswith("# format"):
                format_counter += 1

            # 第一段 org_id|changed|org_name|country|source
            if format_counter == 1:  # 将组织和国家/地区对应
                org_id = line.split('|')[0]
                country = line.split('|')[-2]
                org_country[org_id] = country

            if format_counter == 2:  # 第二段
                asn = line.split('|')[0]
                org_id = line.split('|')[3]
                name = line.split('|')[2]
                org_asn[org_id].append(asn)  # org_asn[org_id]表示org_id管理的的asn的列表
                asn_org[asn] = org_id
                asn_name[asn] = name


# 解析as_path.txt文件，生成边数据
def write_edges(filepath, type):
    f = open(filepath)
    line = f.readline()
    while line:
        if line[0] != '#':  # 跳过 # 开头的
            line = line.split('|')
            as1 = int(line[0])
            as2 = int(line[1])

            # 筛选条件：asn所属国家/地区
            c1 = org_country[asn_org[str(as1)]]
            c2 = org_country[asn_org[str(as2)]]

            areaSet = []
            if area == area_list[0]:  # 仅中国
                areaSet = ['CN', 'TW', 'HK', 'MO']
                # 如果选择中国，那么只需要筛选 c1在中国里，c2不在中国的就行了。只要节点。
                if c1 in areaSet and c2 not in areaSet:
                    outdegreeMap[as1] += 1
                    set_c.add(as1)
            elif area == area_list[1]:  # 美国
                areaSet = ['US']
                if c1 in areaSet and c2 not in areaSet:
                    outdegreeMap[as1] += 1
                    set_c.add(as1)

            # elif area == area_list[2]:  # 中美
            #     areaSet = ['CN', 'TW', 'HK', 'MO', 'US']
            #     # 如果是中美的话，


            # # 全世界范围内的，不作限制 或 这一条边的两个节点都在这个范围内
            # if area == area_list[0] or {c1, c2}.issubset(areaSet):
            #     outdegreeMap[as1] += 1
            #     indegreeMap[as2] += 1
            #     set_c.add(as1)
            #     set_c.add(as2)
            #
            #     # 如果是ipv4直接写入，如果是ipv6，先找有没有ipv4，如果有 修改。 如果没有 写入
            #     if type == 'ipv4':
            #         buffer[(as1, as2)] = type
            #     else:
            #         if buffer.get((as1, as2)) != None:  # 已有ipv4的边，修改
            #             buffer[(as1, as2)] = 'ipv4&6'
            #         else:
            #             buffer[(as1, as2)] = type  # 添加新的ipv6
            #
            # else:  # 只有1个节点在。此时不加边，只加出度/入度
            #     if c1 in areaSet:  # 只有 c1 -> 其他区域，把c1的出度算进去，另一个节点不放入。
            #         outdegreeMap[as1] += 1
            #         set_c.add(as1)
            #     elif c2 in areaSet:
            #         indegreeMap[as2] += 1  # 只有其他区域-> c2，把c2的入度算进去，另一个节点不放入
            #         set_c.add(as2)


        line = f.readline()  # 继续读下一行
    f.close()


def mag(deg):
    if deg < 10:
        return 1
    elif deg < 100:
        return 2
    elif deg < 1000:
        return 3
    elif deg < 10000:
        return 4
    else:
        return 5


if __name__ == '__main__':
    nodeCSV = open("./outputs_CN_US/filtered_nodes_" + mode + '_' + year + '_' + area + ".csv", 'w', encoding='utf8')

    nodeWriter = csv.writer(nodeCSV)

    nodeTitle = ['id', 'label', 'name', 'degree', 'outdegree','org', 'country', 'mag']

    nodeWriter.writerow(nodeTitle)

    dealCountry('./resources/' + year + '0101.as-org2info.txt')
    set_c = set()
    outdegreeMap = defaultdict(int)
    indegreeMap = defaultdict(int)

    if mode == 'ipv4&6':
        filepath = './outputs/' + 'ipv4' + '_' + year + '_as_path.txt'
        write_edges(filepath, 'ipv4')
        filepath = './outputs/' + 'ipv6' + '_' + year + '_as_path.txt'
        write_edges(filepath, 'ipv6')
    else:
        filepath = './outputs/' + mode + '_' + year + '_as_path.txt'
        write_edges(filepath, mode)


    set_c = list(set_c)

    for key in set_c:
        org_id = asn_org[str(key)]
        country = org_country[org_id]
        name = asn_name[str(key)]
        outdegree = outdegreeMap[key]
        indegree = indegreeMap[key]

        degree = outdegree + indegree

        # id, label, 度，出度，org_id, country，量级
        row_content = [key, str(key), name, degree, outdegree, org_id, country, mag(outdegree)]
        print(row_content)
        nodeWriter.writerow(row_content)

    nodeCSV.close()
