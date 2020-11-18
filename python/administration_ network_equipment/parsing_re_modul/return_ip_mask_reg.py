# -*- coding: utf-8 -*-
"""
function get_ip_from_cfg, argue - name file with config,
return values :
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]
"""
import re

def get_ip_from_cfg(file_name):
    list_out = []
    regular_actet = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    with open(file_name, "r") as file:
        for line in file:
            match_ip_mask = re.search(
                'ip\saddress\s' + (regular_actet + '\.') * 3 + regular_actet + '\s' + (regular_actet + '\.') * 3
                + regular_actet, line)
            if match_ip_mask:
                ip_mask = tuple(match_ip_mask.group().replace("ip address", '').split(' ')[1:])
                list_out.append(ip_mask)
    return list_out
print(get_ip_from_cfg("config_r1.txt"))

"""new var"""
def get_ip_from_cfg(config):
    regex = r"ip address (\S+) (\S+)"
    with open(config) as f:
        result = [m.groups() for m in re.finditer(regex, f.read())]
    return result