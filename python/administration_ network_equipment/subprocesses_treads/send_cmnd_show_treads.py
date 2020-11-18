# -*- coding: utf-8 -*-
"""
Задание 20.2

function send_show_command_to_devices, sendу show .

Параметры функции:
* devices - list device params
* command - comand
* filename - file dump out log
* limit - max treads, default 3


out example:
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

use params devices.yaml
"""
from itertools import repeat

from netmiko import ConnectHandler
import yaml
from concurrent.futures import ThreadPoolExecutor


def send_command(device, command):
    data = list()
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        res = str(ssh.find_prompt() + command)
        result = ssh.send_command(command)
        data.append(res)
        data.append(result)
    return data


def send_show_command_to_devices(devices, command, filename, limit=3):
    data = list()

    with ThreadPoolExecutor(max_workers=limit) as worker:
        result = worker.map(send_command, devices, repeat(command))
    for device, items in zip(devices, result):
        data.extend(items)
    with open(filename, "w+") as f:
        for i in data:
            f.writelines("\n" + i)


if __name__ == "__main__":
    command = "show ip int br"
    filename = "data_save"
    with open("devices.yaml") as f:
        devise_list = yaml.safe_load(f)
    send_show_command_to_devices(devise_list, command, filename)

#refactor
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from netmiko import ConnectHandler
import yaml


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"


def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(send_show_command, devices, repeat(command))
        with open(filename, "w") as f:
            for output in results:
                f.write(output)


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_show_command_to_devices(devices, command, "result.txt")