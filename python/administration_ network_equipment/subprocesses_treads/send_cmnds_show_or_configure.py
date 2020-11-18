# -*- coding: utf-8 -*-
"""
send_commands_to_devices, send show or config to different devices and then write .

params:
* devices - dict list
* filename - file to write log
* show - comand show in default None
* config - comands configuration, default None
* limit - max treads

out example:
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


In [5]: send_commands_to_devices(devices, show='sh clock', filename='result.txt')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, config='logging 10.5.5.5', filename='result.txt')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: send_commands_to_devices(devices,
                                  config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                                  filename='result.txt')

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
"""
from itertools import repeat

from netmiko import ConnectHandler
import yaml
from concurrent.futures import ThreadPoolExecutor


def show_command(device, show):
    data = list()
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        res = str(ssh.find_prompt() + show)
        result = ssh.send_command(show)
        data.append(res)
        data.append(result)
    return data


def config_command(device, config):
    data = list()
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_config_set(config)
        data.append(result)
    return data


def send_commands_to_devices(devices, filename, show=None, config=None,  limit=3):
    data = list()

    with ThreadPoolExecutor(max_workers=limit) as worker:
        if show:
            result = worker.map(show_command, devices, repeat(show))
        elif config:
            result = worker.map(config_command, devices, repeat(config))
        else:
            print("NO COMMANDS IMPUT")
    for device, items in zip(devices, result):
        data.extend(items)
    with open(filename, "w+") as f:
        for i in data:
            f.writelines("\n" + i)


if __name__ == "__main__":
    command = 'sh clock'
    command_conf = ["logging 10.5.5.5", ]
    filename = "data_save"
    with open("devices.yaml") as f:
        devise_list = yaml.safe_load(f)
    send_commands_to_devices(devise_list, filename, config=command_conf)

#alternative
def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"


def send_cfg_commands(device, commands):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_config_set(commands)
    return result


def send_commands_to_devices(devices, filename, show=None, config=None, limit=3):
    command = show if show else config
    function = send_show_command if show else send_cfg_commands

    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(function, device, command) for device in devices]
        with open(filename, "w") as f:
            for future in as_completed(futures):
                f.write(future.result())


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.load(f)
    send_commands_to_devices(devices, show=command, filename="result.txt")
    send_commands_to_devices(devices, config="logging 10.5.5.5", filename="result.txt")