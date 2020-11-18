# -*- coding: utf-8 -*-
"""
function  get_ints_without_description, argue - name file with config.
return list interfaces without description
with:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth
no description:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255
"""
import re

# old ver
def get_ints_without_description(file_name):
    out_int_non_descr = []
    regular_pattern = "(interface\s+\S+)"
    regular_pattern2 = r"(interface\s+\S+)\n.\w+\s+\w+"
    with open(file_name, "r") as file:
        a = file.read().split("!")
        for i in a:
            match = re.search(regular_pattern2, i)
            if match and "description" not in match.group():
                interface = re.search(regular_pattern, match.group())
                out_int_non_descr.append(interface.group().replace("interface ", ""))
    return out_int_non_descr[:-1]
get_ints_without_description("config_r1.txt")

# refactored
def get_ints_without_description(config):
    regex = re.compile(r"!\ninterface (?P<intf>\S+)\n"
                       r"(?P<descr> description \S+)?")
    with open(config) as src:
        match = regex.finditer(src.read())
        result = [m.group('intf') for m in match if m.lastgroup == 'intf']
        return result