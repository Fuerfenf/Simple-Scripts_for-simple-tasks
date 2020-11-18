# -*- coding: utf-8 -*-
"""
function takes: 

- intf_vlan_mapping:
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
     'FastEthernet0/4': [17]}
- trunk_template:  trunk_mode_template

return dictionary:
    {key = interface name} : {value = commands list}
"""

trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}

def formate_line(line, val):

    if "trunk allowed vlan" in line:
        liststr = list()
        for itm in val:
            liststr.append(str(itm))
        return line.replace("trunk allowed vlan", "trunk allowed vlan {}".format(",".join(liststr)))
    else:
        return line

def formate_command(trunk, val):

    commands = list()
    for line in trunk:
        commands.append(formate_line(line, val))
    return commands

def generate_trunk_config(intf_vlan_mapping, trunk_template):

    out_list = dict()
    for key, val in intf_vlan_mapping.items():
        out_list[key] = (formate_command(trunk_template, val))

    return out_list

a = generate_trunk_config(trunk_config, trunk_mode_template)
print(a)

"""
alternative
"""
def generate_trunk_config(intf_vlan_mapping, trunk_template):
    trunk_conf = {}
    for port, vlans in intf_vlan_mapping.items():
        commands = []
        for command in trunk_template:
            if command.endswith("allowed vlan"):
                vlans_str = ",".join([str(vl) for vl in vlans])
                commands.append(f"{command} {vlans_str}")
            else:
                commands.append(command)
        trunk_conf[port] = commands
    return trunk_conf

