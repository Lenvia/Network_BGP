import csv
from collections import defaultdict

mode = 'ipv4&6'
year = '2021'
area_list = ['all', 'CH', 'US', 'CH&US'] # 地区
area = area_list[1]


org_asn = defaultdict(list)  # 组织所管辖的AS列表
asn_org = defaultdict(str)  # AS编号到组织的映射
org_country = defaultdict(str)  # 组织到国家/地区的映射

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
                org_asn[org_id].append(asn)  # org_asn[org_id]表示org_id管理的的asn的列表
                asn_org[asn] = org_id


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
            if area == area_list[1]:  # 仅中国
                areaSet = ['CH', 'TW', 'HK', 'MO']
            elif area == area_list[2]:  # 美国
                areaSet = ['US']
            elif area == area_list[3]:  # 中美
                areaSet = ['CH', 'TW', 'HK', 'MO', 'US']

            if area == area_list[0] or c1 in areaSet:                
                outdegreeMap[as1] += 1
                
            if area == area_list[0] or {c1, c2}.issubset(areaSet):
                set_c.add(as1)
                set_c.add(as2)

                indegreeMap[as2] += 1

                # 如果是ipv4直接写入，如果是ipv6，先找有没有ipv4，如果有 修改。 如果没有 写入
                if type == 'ipv4':
                    buffer[(as1, as2)] = type
                else:
                    if buffer.get((as1, as2)) != None:  # 已有ipv4的边，修改
                        buffer[(as1, as2)] = 'ipv4&6'
                    else:
                        buffer[(as1, as2)] = type  # 添加新的ipv6

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
    edgeCSV = open("./outputs/edges_"+mode+'_'+year+'_'+area+".csv", 'w', encoding='utf8')
    nodeCSV = open("./outputs/nodes_"+mode+'_'+year+'_'+area+".csv", 'w', encoding='utf8')

    nodeWriter = csv.writer(nodeCSV)
    edgeWriter = csv.writer(edgeCSV)

    nodeTitle = ['id', 'label', 'degree', 'outdegree', 'indegree', 'org', 'country', 'score', 'mag']
    edgeTitle = ['source', 'target', 'mode', 'sourceOutdegree', 'mag']

    nodeWriter.writerow(nodeTitle)
    edgeWriter.writerow(edgeTitle)

    dealCountry('./resources/'+year+'0101.as-org2info.txt')
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

    for item in buffer:
        # as1, as2, type, as1的出度
        edgeWriter.writerow([item[0], item[1], buffer[item], outdegreeMap[item[0]], mag(outdegreeMap[item[0]])])
    edgeWriter.writerow([1000000, 1000001, 0, 0, 5])
    edgeWriter.writerow([1000000, 1000002, 0, 0, 4])
    edgeWriter.writerow([1000000, 1000003, 0, 0, 3])
    edgeWriter.writerow([1000000, 1000004, 0, 0, 2])
    edgeWriter.writerow([1000000, 1000000, 0, 0, 1])
    edgeCSV.close()

    set_c = list(set_c)

    for key in set_c:
        org_id = asn_org[str(key)]
        country = org_country[org_id]
        outdegree = outdegreeMap[key]
        indegree = indegreeMap[key]
        degree = outdegree+indegree
        

        # id, label, 度，出度，入度，org_id, country, score（暂时没用）
        row_content = [key, str(key), degree, outdegree, indegree, org_id, country, 0, mag(outdegree)]
        nodeWriter.writerow(row_content)
        
    nodeWriter.writerow([1000000, 0, 0, 0, 0, 0, 0, 0, 5])
    nodeWriter.writerow([1000001, 0, 0, 0, 0, 0, 0, 0, 4])
    nodeWriter.writerow([1000002, 0, 0, 0, 0, 0, 0, 0, 3])
    nodeWriter.writerow([1000003, 0, 0, 0, 0, 0, 0, 0, 2])
    nodeWriter.writerow([1000004, 0, 0, 0, 0, 0, 0, 0, 1])
    nodeCSV.close()
