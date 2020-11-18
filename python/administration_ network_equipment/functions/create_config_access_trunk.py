# -*- coding: utf-8 -*-
"""
function get_int_vlan_map, process config file switch return list {key= port name : value= vlans on port}:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}
for trunck:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}
base set port as: 
            interface FastEthernet0/20
                switchport mode access
                duplex auto
     port in  VLAN 1
   this variant for out:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

function tacke 1 param file - config_sw2.txt.
"""

def get_int_vlan_map(config_filename):

    dickt_trunk = dict()
    dickt_access = dict()
    interface = None

    with open(config_filename, "r") as file:
        config = file.read()
        conf_list = config.split("!")
        formated_conf_list = list()

        for itm in conf_list:
            if itm != "\n":
                formated_conf_list.append(itm)

        for elment in formated_conf_list:
            if "interface FastEthernet" in elment:
                if "switchport access vlan" in elment:
                    commands = elment.split("\n")
                    for itm in commands:
                        if "interface FastEthernet" in itm:
                            interface = itm.replace("\n", "").replace("interface ", "")
                        if "switchport access vlan" in itm:
                            dickt_access[interface] = int(itm.replace("\n", "")[-2:])
                elif "switchport trunk allowed" in elment:
                    vlan_tr = list()
                    commands = elment.split("\n")
                    for itm in commands:
                        if "interface FastEthernet" in itm:
                            interface = itm.replace("\n", "").replace("interface ", "")
                        if "switchport trunk allowed" in itm:
                            vlan_trunk = itm.replace("\n", "").split(" ")[-1]
                            vlan_trunk = vlan_trunk.split(",")
                            for itms in vlan_trunk:
                                vlan_tr.append(int(itms))
                            dickt_trunk[interface] = vlan_tr
                else:
                    commands = elment.split("\n")
                    for itm in commands:
                        if "interface FastEthernet" in itm:
                            interface = itm.replace("\n", "").replace("interface ", "")
                        if "switchport mode access" in itm:
                            dickt_access[interface] = 1

        return dickt_access, dickt_trunk
"""
alternative
"""
def get_int_vlan_map(config_filename):
    access_port_dict = {}
    trunk_port_dict = {}
    with open(config_filename) as f:
        for line in f:
            if "interface FastEthernet" in line:
                current_interface = line.split()[-1]
                # interface is vlan 1 access_port_dict
                access_port_dict[current_interface] = 1
            elif "switchport access vlan" in line:
                # if other VLAN, change value
                access_port_dict[current_interface] = int(line.split()[-1])
            elif "switchport trunk allowed vlan" in line:
                vlans = [int(i) for i in line.split()[-1].split(",")]
                trunk_port_dict[current_interface] = vlans
                # if  trunk allowed vlan delete from access_port_dict
                del access_port_dict[current_interface]
    return access_port_dict, trunk_port_dict