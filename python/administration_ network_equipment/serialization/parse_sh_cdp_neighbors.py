# -*- coding: utf-8 -*-
"""
function parse sh_cdp_neighbors, parced show cdp neighbors.
-take arg line from show cdp neighbors 
-return dict with connections between devices
in date:
R4>show cdp neighbors
Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0
return data:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}
file sh_cdp_n_sw1.txt
"""
import re

def parse_sh_cdp_neighbors(cdp_n_sw):
    out_dict = dict()
    local_int = list()
    dict_inner = list()
    re_device = "(?P<device>\S+).show"
    device = re.search(re_device, cdp_n_sw)["device"]
    re_neigbr = "(?P<device>\S+)\s+(?P<Lintface>Eth\s+\d+.\d+)\s+\d*\s+\w\s\w\s\w\s+\d+\s+(?P<Dintface>Eth\s+\d+.\d+)"
    data = cdp_n_sw.split("\n")

    for itm in data[7:]:
        row = re.search(re_neigbr, itm)
        if row:
            dev_id = row["device"]
            local_int.append(row["Lintface"])
            dst_int = row["Dintface"]
            dict_inner.append({dev_id: dst_int})
    compare = dict(zip(local_int, dict_inner))
    out_dict[device] = compare
    return out_dict


with open("sh_cdp_n_sw1.txt", "r") as file:
    data = file.read()

print(parse_sh_cdp_neighbors(data))

# alternative 
def parse_sh_cdp_neighbors2(command_output):
    regex = re.compile(
        r"(?P<r_dev>\w+)  +(?P<l_intf>\S+ \S+)"
        r"  +\d+  +[\w ]+  +\S+ +(?P<r_intf>\S+ \S+)"
    )
    connect_dict = {}
    l_dev = re.search(r"(\S+)[>#]", command_output).group(1)
    connect_dict[l_dev] = {}
    for match in regex.finditer(command_output):
        r_dev, l_intf, r_intf = match.group("r_dev", "l_intf", "r_intf")
        connect_dict[l_dev][l_intf] = {r_dev: r_intf}
    return connect_dict


if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        print(parse_sh_cdp_neighbors(f.read()))