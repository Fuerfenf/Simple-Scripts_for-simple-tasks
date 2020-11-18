# -*- coding: utf-8 -*-
"""
Задание 7.2c
process file gived it as argue :
    - name input file
    - name output file
    - filter lines with ignire
    - write result in out file
"""
from sys import argv

ignore = ["duplex", "alias", "Current configuration"]
file_name = argv[1]
file_save = argv[2]
if file_name and file_save:
    with open(file_name, "r") as file:
        my_file = open(file_save, "w")
        for itm in file.readlines():
            if not (set(ignore)) & set(itm.split()) and ignore[2] not in itm:
                my_file.write(itm)
        my_file.close()

