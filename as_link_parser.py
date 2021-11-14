mode = 'ipv6'
year = '2019'
file = './middle/'+mode+'_'+year+'_sanitized_rib.txt'

with open(file) as f:
    wf = open('./outputs/'+mode+'_'+year+'_as_path.txt', "w")
    link_set = set("")
    for line in f:
        asn_list = line.strip().split("|")
        for i in range(1, len(asn_list)):
            link = str(asn_list[i - 1]) + "|" + str(asn_list[i])
            if link in link_set:
                continue
            link_set.add(link)
            wf.write(link + "\n")
