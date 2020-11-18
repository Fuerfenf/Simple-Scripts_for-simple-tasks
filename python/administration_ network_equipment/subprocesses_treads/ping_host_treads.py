# -*- coding: utf-8 -*-
"""
function ping_ip_addresses, ping ip in diff treads.
params:
* ip_list - ip list
* limit - max treads , default= 3
return tuple with lists:
reachable, unreachable
used in commnd line ping.
"""
import subprocess
import os
import yaml
from concurrent.futures import ThreadPoolExecutor

def ping_ip_addresses(ip_list, limit=3):
    list_avalible = list()
    list_not_avalible = list()

    def pinging(ip):
        status, response = subprocess.getstatusoutput("ping -c2 " + ip)
        if status == 0:
            list_avalible.append(ip)
        else:
            list_not_avalible.append(ip)

    with ThreadPoolExecutor(max_workers=limit) as worker:
        for ip in ip_list:
            worker.submit(pinging, ip)

    return list_avalible, list_not_avalible


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devise_list = [i['ip'] for i in yaml.safe_load(f)]
    ping_ip_addresses(devise_list)



