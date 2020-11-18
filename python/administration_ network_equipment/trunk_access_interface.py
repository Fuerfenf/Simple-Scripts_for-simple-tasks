# -*- coding: utf-8 -*-
"""
input work mode (access/trunk): access
input type and mode for interface: Fa0/6
input number of vlan(s): 3
example outlines: 

interface Fa0/6
switchport mode access
switchport access vlan 3
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable

interface Fa0/7
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 2,3,4,5
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]

type_vlan = {
            "access": 'Введите номер VLAN: ',
            "trunk": 'Введите разрешенные VLANы: '
            }

out = []

interface_mode = input("Введите режим работы интерфейса (access/trunk): ")
interface_ = input("Введите тип и номер интерфейса: ")
vlan_stack = input(type_vlan[interface_mode])
access_template[1] = access_template[1].format(vlan_stack)
trunk_template[2] = trunk_template[2].format(vlan_stack)
out.append("interface {}".format(interface_))
out.extend(access_template)
out_line = '\n'.join(out)

"""
alternative way
"""
template = {"access": access_template, "trunk": trunk_template}
mode = input("Enter interface mode (access/trunk): ")
interface = input("Enter interface type and number: ")
vlans = input(type_vlan[mode])
out_line = "interface {}\n".format(interface) + "\n".join(template[mode]).format(vlans)

#------------------------------------------------------------------------------------------------------------

"""
generate pattern for access and trunk ports

example trunk command and vlan list:
	['add', '10', '20'] - команда switchport trunk allowed vlan add 10,20
	['del', '17'] - команда switchport trunk allowed vlan remove 17
	['only', '11', '30'] - команда switchport trunk allowed vlan 11,30
"""

access_template = [
    "switchport mode access",
    "switchport access vlan",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan",
]
access = {"0/12": "10", "0/14": "11", "0/16": "17", "0/17": "150"}
trunk = {"0/1": ["add", "10", "20"], "0/2": ["only", "11", "30"], "0/4": ["del", "17"]}
# first way
for intf, value in trunk.items():
    print(f"interface FastEthernet {intf}")
    for command in trunk_template:
        if command.endswith("allowed vlan"):
            action = value[0]
            vlans = ",".join(value[1:])

            if action == "add":
                print(f" {command} add {vlans}")
            elif action == "only":
                print(f" {command} {vlans}")
            elif action == "del":
                print(f" {command} remove {vlans}")
        else:
            print(" {}".format(command))
# other used dictionary
trunk_actions = {"add": "add", "del": "remove", "only": ""}
for intf, value in trunk.items():
    print(f"interface FastEthernet {intf}")

    for command in trunk_template:
        if command.endswith("allowed vlan"):
            action = value[0]
            vlans = ",".join(value[1:])
            print(f" {command} {trunk_actions[action]} {vlans}")
        else:
            print(f" {command}")


