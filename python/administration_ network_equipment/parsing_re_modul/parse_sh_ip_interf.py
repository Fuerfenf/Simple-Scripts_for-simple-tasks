# -*- coding: utf-8 -*-
"""
function parse_sh_ip_int_br,  argue - name file with outline show ip int br
return :
* Interface
* IP-Address
* Status
* Protocol
look like:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]
use file sh_ip_int_br.txt.
"""
import re

def parse_sh_ip_int_br(file_name):
    out_list = []
    with open(file_name, "r") as file:
        regular_actet = """(?P<interface>\S+) +(?P<ip>\S+) +(?P<ok>\S+) +(?P<method>\S+) +(?P<status>.+\S+) +(?P<protocol>\S+)"""
        for line in file:
            match = re.search(regular_actet, line)
            if match:
                parametrs = match.groupdict()
                out_list.append((parametrs["interface"], parametrs["ip"], parametrs["status"], parametrs["protocol"]))
    return out_list[1:]

print(parse_sh_ip_int_br("sh_ip_int_br.txt"))

# shortest way
def parse_sh_ip_int_br(textfile):
    regex = r"(\S+) +(\S+) +\w+ \w+ +(administratively down|up|down) +(up|down)"
    with open(textfile) as f:
        result = [m.groups() for m in re.finditer(regex, f.read())]
    return result