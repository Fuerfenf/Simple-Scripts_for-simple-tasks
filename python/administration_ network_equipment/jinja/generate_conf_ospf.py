# -*- coding: utf-8 -*-
"""
templates/ospf.txt based on ospf in  cisco_ospf.txt.

attr:
* process name. name - process
* router-id. name - router_id
* reference-bandwidth. name - ref_bw
* interfase up in OSPF. name - ospf_intf
 * dickt list with next keys:
  * name - interface name, as Fa0/1, Vlan10, Gi0/0
  * ip - IP-addr, as 10.0.1.1
  * area - zone number
  * passive - active or passive : True/False
all interface ospf_intf, generate next lines:
 network x.x.x.x 0.0.0.0 area x
if passive:
 passive-interface x
if active:
 ip ospf hello-interval 1

templates/ospf.txt, test on ddata from data_files/ospf.yml,
function  generate_config  from generate_config
Не копируйте код функции generate_config.


"""
from generate_config import *
from generate_config import generate_config
import yaml


if __name__ == "__main__":
    path_template = "templates/ospf.txt"
    with open('data_files/ospf.yml') as file:
        devices = yaml.safe_load(file)
    print(generate_config(path_template, devices))