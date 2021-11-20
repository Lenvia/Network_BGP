# Network_BGP

## 项目介绍

xxxxxx



## 项目结构

├── README.md
├── analysis
│  ├── CN_US_analysis.py  // 生成中美AS分布折线图
│  ├── CN_US_analysis_filter.py  // 生成过滤后的中美AS分布折线图
│  ├── csv_analysis.py  // 生成IPv6时间变化折线图
│  ├── global_analysis.py  // 生成全球AS分布折线图
│  ├── rank_analysis.py  // 生成2020-2021年IPv6出度和排名变化折线图
│  └── v4_v6_analysis.py  // 生成IPv4和IPv6分布折线图
├── as_link_parser.py  // 将路径拆分为最小片段
├── bgp_path_downloader.py  // 下载数据并处理
├── bgp_path_parser.py  // 使用peeringdb对IXP进行过滤
├── generate_data_CN&US.py  // 产生过滤中美AS的结点和边，存储为CSV
├── generate_data_sameYear.py  // 产生其他所有情况的结点和边，存储为CSV
└── requirements.txt  // 库



## 流程

### 安装依赖库

```
pip install -r requirements.txt
```

参考[引导](https://bgpstream.caida.org/download)安装 BGPStream V2，再安装pybgpstream==2.0.2



### 下载rib

使用脚本 **bgp_path_downloader.py** 下载BGP paths （来自 RouteViews 和 RIPE NCC）

修改 **downloader()** 函数 中 mode 和 year 来指定类型和时间，例如

```
mode = 'ipv4'
year = '2019'
```



### 从CAIDA下载 AS-组织 映射数据

https://www.caida.org/data/as-organizations/

在根目录创建resourses文件夹，并放入该目录下



### 从CAIDA下载PeeringDB数据集

2016年3月前: http://data.caida.org/datasets/peeringdb-v1/

2016年3月后: http://data.caida.org/datasets/peeringdb/

放入resourses文件夹下



### 解析 BGP path

修改 **bgp_path_parser.py** 中的 mode 和 year 来指定类型和年份。

并在main函数中指明peeringdb的存放路径，如

```
peeringdb = './resources/peeringdb_2_dump_2021_01_01.json'
```

（将产生sanitized_rib.txt文件，如 "ipv4_2021_sanitized_rib.txt"



### 将路径拆分为最小片段

在 **as_link_parser.py** 中指明 mode 和 year，以及上一步骤下产生的文件 sanitized_rib.txt 的路径



### 产生所需的结点和边表格

在 **generate_data_sameYear.py** 及 **generate_data_CN&US.py** 中指明类型、年份和筛选的地区

```
mode = 'ipv4&6'
year = '2021'
area = area_list[0]
```



### 绘制拓扑图

将上一步骤产生的结点和边表格导入到Gephi软件并绘制，这里不做介绍。



### 生成分布折线图

按需从analysis文件夹下选择合适的脚本进行生成。





## 联络

- [Yuxuan Chen](https://github.com/chenyxuan)
- [Runpu Yue](https://github.com/Lenvia)

若使用过程中出现任何问题，可以通过以下邮箱联系我们

chenyuxuan21@mails.ucas.ac.cn

yuerunpu21@mails.ucas.ac.cn

