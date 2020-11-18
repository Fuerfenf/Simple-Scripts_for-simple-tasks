# -*- coding: utf-8 -*-

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        _norm_dict = dict()
        for key, value in topology_dict.items():
            if not _norm_dict.get(value) == key:
                _norm_dict[key] = value
        return _norm_dict

    def delete_link(self, *del_link):
        list_key = list()
        for key, value in self.topology.items():
            if key == del_link[0] and value == del_link[1]:
                list_key.append(key)
            elif key == del_link[1] and value == del_link[0]:
                list_key.append(key)
            else:
                print("Такого соединения нет")
        for itm in list_key:
            del self.topology[itm]

top = Topology(topology_example)
top.topology
top.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
top.topology