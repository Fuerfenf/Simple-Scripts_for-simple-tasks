# -*- coding: utf-8 -*-
"""
function create_network_map, parse show cdp neighbors from diff files and compare in one topology.
function params : filenames, file list, in files out from command show cdp neighbors.
return dict:
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
generate topology for files:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
create_network_map, clear duples.
draw_topology from draw_network_graph.py draw scheme topology from create_network_map.
Результат должен выглядеть так же, как схема в файле task_11_2a_topology.svg

modul used graphviz
"""
from draw_network_graph import draw_topology


def pattern(command_line):
    glob_list = list()
    for data in command_line:
        if ">" in data:
            line = data.split(">")[0]
            main_device = [line.replace("\n", "") if "\n" in line else line][0]
        com_line = data.split("\n")
        point_slice = [com_line.index(itm) for itm in com_line if "Device ID" in itm][0]
        glob_list.append([main_device, com_line[point_slice+1:]])
    return glob_list


def delete_dubles(base_dict):
    unic_dict = dict()
    for base_key in base_dict.keys():
        if "SW" in base_key[0]:
            if not unic_dict.get(base_dict[base_key]):
                unic_dict[base_dict[base_key]] = base_key
        else:
            if not unic_dict.get(base_key):
                unic_dict[base_key] = base_dict[base_key]
    return unic_dict


def create_network_map(filenames):
    readed_files = grep_lines(filenames)
    parsed_data = dict()
    data_from_files = pattern(readed_files)
    for data in data_from_files:
        for itm_line in data[1]:
            if itm_line:
                device_port = [itm for itm in itm_line.split(" ") if itm]
                loc_int = "".join(device_port[1:3])
                port_id = "".join(device_port[-2:])
                parsed_data[(data[0], loc_int)] = (device_port[0], port_id)
    return delete_dubles(parsed_data)


def grep_lines(files):
    file_commands = list()
    for file in files:
        with open(file, "r") as file:
            data = file.read()
            file_commands.append(data)
    return tuple(file_commands)


if __name__ == "__main__":
    infiles = [
        "sh_cdp_n_sw1.txt",
        "sh_cdp_n_r1.txt",
        "sh_cdp_n_r2.txt",
        "sh_cdp_n_r3.txt"
        ]
    topology_data = create_network_map(infiles)
    for k, v in topology_data.items():
        print(k, v)
    draw_topology(topology_data)
    
"""
alternative var
"""
from task_11_1 import parse_cdp_neighbors
from draw_network_graph import draw_topology
from pprint import pprint

def create_network_map(filenames):
    network_map = {}

    for filename in filenames:
        with open(filename) as show_command:
            parsed = parse_cdp_neighbors(show_command.read())
            for key, value in parsed.items():
                if not network_map.get(value) == key:
                    network_map[key] = value
    return network_map
# and other
def create_network_map(filenames):
    network_map = {}

    for filename in filenames:
        with open(filename) as show_command:
            parsed = parse_cdp_neighbors(show_command.read())
            for key, value in parsed.items():
                key, value = sorted([key, value])
                network_map[key] = value
    return network_map


if __name__ == "__main__":
    infiles = [
        "sh_cdp_n_sw1.txt",
        "sh_cdp_n_r1.txt",
        "sh_cdp_n_r2.txt",
        "sh_cdp_n_r3.txt",
    ]

    topology = create_network_map(infiles)
    pprint(topology)
    draw_topology(topology)