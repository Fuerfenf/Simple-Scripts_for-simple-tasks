# -*- coding: utf-8 -*-
"""
formate from CAM_table.txt.
to
 100    01bb.c580.7000   Gi0/1
 200    0a4b.c380.7000   Gi0/2
 300    a2ab.c5a0.7000   Gi0/3
 100    0a1b.1c80.7000   Gi0/4
 500    02b1.3c80.7000   Gi0/5
 200    1a4b.c580.7000   Gi0/6
 300    0a1b.5c80.7000   Gi0/7
- user input vlan
- return needed vlan info 
"""

user_vlan = input("Enter VLAN number: ")

with open("CAM_table.txt", "r") as conf:
    for line in conf:
        line = line.split()
        if line and line[0].isdigit() and line[0] == user_vlan:
            vlan, mac, _, intf = line
            line = f"{vlan:9}{mac:20}{intf}"

