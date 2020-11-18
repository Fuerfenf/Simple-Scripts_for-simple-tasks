# -*- coding: utf-8 -*-
"""
Задание 9.1a


generate access-port function take:
- dictionary:
    {'FastEthernet0/12':10,
     'FastEthernet0/14':11,
     'FastEthernet0/16':17}
- patternt command list - access_mode_template
return list all ports in access used pattern access_mode_template
out list as:
[
'interface FastEthernet0/12',
'switchport mode access',
'switchport access vlan 10',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable',
'interface FastEthernet0/17',
'switchport mode access',
'switchport access vlan 150',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable',
...]

add alter param with set port-security (psecurity in base = None)
for configurate port-security used trmplate port_security_template
"""

access_mode_template = [
    "switchport mode access",
    "switchport access vlan",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

port_security_template = [
    "switchport port-security maximum 2",
    "switchport port-security violation restrict",
    "switchport port-security",
]

access_config = {"FastEthernet0/12": 10, "FastEthernet0/14": 11, "FastEthernet0/16": 17}


def formate_access(line, vl):

    if "access vlan" in line:
        return line.replace("access vlan", "access vlan {}".format(vl))
    else:
        return line


def generate_access_config(intf_vlan_mapping, access_template, psecurity=None):
    out_list = list()
    for intf, vlan in intf_vlan_mapping.items():
        out_list.append("interface {}".format(intf))
        for commands in access_template:
            out_list.append(formate_access(commands, vlan))
        if psecurity:
            for item in port_security_template:
                out_list.append(item)
        for commands in out_list:
            if "access vlan" in commands:
                commands.replace("access vlan", "access vlan {}".format(vlan))
    return out_list


out = generate_access_config(access_config, access_mode_template)
for itm in out:
    print(itm)

psecurity = True
out = generate_access_config(access_config, access_mode_template, psecurity)
for itm in out:
    print(itm)

"""
alternative way
"""
def generate_access_config(intf_vlan_mapping, access_template, psecurity=None):
    access_config = []

    for intf, vlan in intf_vlan_mapping.items():
        access_config.append(f"interface {intf}")
        for command in access_template:
            if command.endswith("access vlan"):
                access_config.append(f"{command} {vlan}")
            else:
                access_config.append(command)
        if psecurity:
            access_config.extend(psecurity)
    return access_config