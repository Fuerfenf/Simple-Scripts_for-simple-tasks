# -*- coding: utf-8 -*-
"""
on base config_r1.txt, create templates:
* templates/cisco_base.txt - all rows beside alias and event manager. name of host - hostname
* templates/alias.txt - template for alias
* templates/eem_int_desc.txt - template for event manager applet
 templates/alias.txt и templates/eem_int_desc.txt.
templates/cisco_router_base.txt. include templates:
* templates/cisco_base.txt
* templates/alias.txt
* templates/eem_int_desc.txt
 templates/cisco_router_base.txt, test by  generate_config из задания 21.1.
data in data_files/router_info.yml
"""
from task_21_1 import *
from task_21_1 import generate_config


if __name__ == "__main__":
    path_template = "templates/cisco_router_base.txt"
    with open('data_files/router_info.yml') as file:
        devices = yaml.safe_load(file)
    print(generate_config(path_template, devices))