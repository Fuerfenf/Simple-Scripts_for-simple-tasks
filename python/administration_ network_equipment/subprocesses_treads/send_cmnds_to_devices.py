# -*- coding: utf-8 -*-
"""
send_command_to_devices, send show diff devices.
params:
* devices - dict list
* commands_dict - dict with comands to device target
* filename - file to write log
* limit - max treads
ecample out:
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


devices devices.yaml and command list commands
"""
from itertools import repeat

from netmiko import ConnectHandler
import yaml
from concurrent.futures import ThreadPoolExecutor


commands = {
    "192.168.100.1": ["sh ip int br", "sh arp"],
    "192.168.100.2": ["sh arp"],
    "192.168.100.3": ["sh ip int br", "sh ip route | ex -"],
}


def send_command(device, commands):
    data = list()
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        cmds = commands[device["ip"]]
        for cmd in cmds:
            res = str(ssh.find_prompt() + cmd)
            result = ssh.send_command(cmd)
            data.append(res)
            data.append(result)
    return data


def send_command_to_devices(devices, commands, filename, limit=3):
    data = list()
    with ThreadPoolExecutor(max_workers=limit) as worker:
        result = worker.map(send_command, devices, repeat(commands))
    for device, items in zip(devices, result):
        data.extend(items)
    with open(filename, "w+") as f:
        for i in data:
            f.writelines("\n" + i)


if __name__ == "__main__":
    filename = "data_save"
    with open("devices.yaml") as f:
        devise_list = yaml.safe_load(f)
    send_command_to_devices(devise_list, commands, filename)
    
#alternative

def send_show_command(device, commands):
    output = ""
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        for command in commands:
            result = ssh.send_command(command)
            prompt = ssh.find_prompt()
            output += f"{prompt}{command}\n{result}\n"
    return output


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = []
        for device in devices:
            ip = device["ip"]
            command = commands_dict[ip]
            futures.append(executor.submit(send_show_command, device, command))
        with open(filename, "w") as f:
            for future in as_completed(futures):
                f.write(future.result())


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.load(f)
    send_command_to_devices(devices, commands, "result.txt")