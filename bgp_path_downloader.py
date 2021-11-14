import datetime
import argparse
from pybgpstream import BGPStream, BGPRecord


def downloader():
    """Download BGP paths from Routeviews and RIPE NCC from a start date for a certain duration."""
    # Create a new bgpstream instance and a reusable bgprecord instance
    stream = BGPStream(
        from_time="2019-01-01 00:00:00", until_time="2019-01-01 00:01:00 UTC",
    )
    # stream.add_interval_filter(base, base + int(duration))
    stream.add_filter('record-type', 'ribs')
    stream.add_filter('ipversion', '6')  # ipv6
    mode = 'ipv6'
    year = '2019'

    stream.start()
    path_set = set()
    print(mode)
    f = open('./middle/'+mode+'_'+year+'_rib.txt', 'w')
    while True:
        rec = stream.get_next_record()
        if rec is None:
            return
        if rec.status != "valid":
            continue
        else:
            elem = rec.get_next_elem()
            while(elem):
                path = elem.fields['as-path']
                if '{' in path or '(' in path:
                    elem = rec.get_next_elem()
                    continue
                prefix = elem.fields['prefix']

                f.write(path.replace(' ', '|') + '\n')
                path_set.add(path)
                elem = rec.get_next_elem()

                # if mode == 'ipv4':
                #     # Focus on IPv4 prefixes
                #     if ":" not in prefix and path not in path_set:
                #         f.write(path.replace(' ', '|') + '\n')
                #         path_set.add(path)
                #     elem = rec.get_next_elem()
                # else:
                #     if ":" in prefix and path not in path_set:
                #         f.write(path.replace(' ', '|') + '\n')
                #         path_set.add(path)
                #     elem = rec.get_next_elem()
    print("end.")
    f.close()


if __name__ == '__main__':
    downloader()
