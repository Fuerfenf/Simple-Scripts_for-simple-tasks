# -*- coding: utf-8 -*-
"""
function  write_dhcp_snooping_to_csv, parced show dhcp snooping binding from diff and write in csv.
args:
* filenames - files with out - show dhcp snooping binding
* output - out file csv
input from *_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2
out csv:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

test on sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.
first coll csv takes from name of files.
"""
import re
import csv
#old
def write_dhcp_snooping_to_csv(filenames, output):

    snooping_data = [["switch", "mac", "ip", "vlan", "interface"]]
    for file_in in filenames:
        re_pattern = "(?P<mac>\w\S+) +(?P<ip>\d\S+) +(?P<lease>\S+) +(?P<type>\S+) +(?P<vlan>\S+) +(?P<intface>\S+)"
        with open(file_in, "r") as file:
            device_name = file_in.split("_")[0]
            for line in file:
                match = re.search(re_pattern, line)
                if match:
                    snooping_data.append([device_name,
                                          match["mac"],
                                          match["ip"],
                                          match["vlan"],
                                          match["intface"]
                                          ])

    with open(output, 'w') as f:
        writer = csv.writer(f)
        for row in snooping_data:
            writer.writerow(row)

write_dhcp_snooping_to_csv(("sw1_dhcp_snooping.txt", "sw2_dhcp_snooping.txt", "sw3_dhcp_snooping.txt"), "output")

#refactored 
def write_dhcp_snooping_to_csv(filenames, output):
    data = []
    regex = r"(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)"
    with open(output, "w") as dest:
        writer = csv.writer(dest)
        writer.writerow(["switch", "mac", "ip", "vlan", "interface"])
        for filename in filenames:
            switch = filename.split("_")[0]
            with open(filename) as f:
                for line in f:
                    match = re.search(regex, line)
                    if match:
                        writer.writerow((switch,) + match.groups())


if __name__ == "__main__":
    write_dhcp_snooping_to_csv(sh_dhcp_snoop_files, "example_csv.csv")