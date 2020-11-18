# -*- coding: utf-8 -*-
"""

function ping_ip_addresses for ping ip take list ip or in last way range 192.168.100.1-10
return list reacheble and list unreacheble ip
"""
import os

list_ip = ['8.8.4.4', '1.1.1.1-3', '172.21.41.130-172.21.41.132']

def convert_ranged_ip(ip_pool):
    ip_list = []
    pool = ip_pool.split('-')
    len_prt = len(pool[1].split(".")[-1])
    if len_prt < 3:
        for ip in range(int(pool[0].split(".")[-1]), int(pool[1]) + 1):
            ip_list.append(pool[0][:-(len(pool[0].split(".")[-1]))] + str(ip))
    else:
        for ip in range(int(pool[0].split(".")[-1]), int(pool[1].split(".")[-1])+1):
            ip_list.append(pool[0][:-(len(pool[0].split(".")[-1]))] + str(ip))
    return ip_list


def convert_ranges_to_ip_list(list_ip):
    deployed_list_ip = []

    for ip_itm in list_ip:
        if "-" in ip_itm:
            for ip in convert_ranged_ip(ip_itm):
                deployed_list_ip.append(ip)
        else:
            deployed_list_ip.append(ip_itm)

    return deployed_list_ip


def ping_ip_addresses(ip_list):
    Reachable = []
    Unreachable = []

    for ip in ip_list:
        response = os.system("ping -c 1 " + ip)
        if response:
            Unreachable.append(ip)
        else:
            Reachable.append(ip)

    return Reachable, Unreachable


returned_list_ip = convert_ranges_to_ip_list(list_ip)
status_ip_list = ping_ip_addresses(returned_list_ip)
"""
alternative
"""
import subprocess


def ping_ip_addresses(ip_addresses):
    list_alive = []
    list_dead = []

    for ip in ip_addresses:
        result = subprocess.run(
            ["ping", "-c", "3", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            list_alive.append(ip)
        else:
            list_dead.append(ip)

    return list_alive, list_dead

if __name__ == "__main__":
    print(ping_ip_addresses(["10.1.1.1", "8.8.8.8"]))
    
#------------------------------------------------------------------------------------------------
"""
ping with range input
"""
def convert_ranges_to_ip_list(ip_addresses):
    ip_list = []
    for ip_address in ip_addresses:
        if "-" in ip_address:
            start_ip, stop_ip = ip_address.split("-")
            if "." not in stop_ip:
                stop_ip = ".".join(start_ip.split(".")[:-1] + [stop_ip])
            start_ip = ipaddress.ip_address(start_ip)
            stop_ip = ipaddress.ip_address(stop_ip)
            for ip in range(int(start_ip), int(stop_ip) + 1):
                ip_list.append(str(ipaddress.ip_address(ip)))
        else:
            ip_list.append(str(ip_address))
    return
    
#------------------------------------------------------------------------------------------------
 """
 return in format
 Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9
 """
reach_ip = ["10.1.1.1", "10.1.1.2"]
unreach_ip = ["10.1.1.7", "10.1.1.8", "10.1.1.9"]
print_ip_table(reach_ip, unreach_ip)

from tabulate import tabulate

def print_ip_table(reach_ip, unreach_ip):
    table = {"Reachable": reach_ip, "Unreachable": unreach_ip}
    print(tabulate(table, headers="keys"))

reach_ip = ["10.1.1.1", "10.1.1.2"]
unreach_ip = ["10.1.1.7", "10.1.1.8", "10.1.1.9"]
print_ip_table(reach_ip, unreach_ip)
# without tabulate
def print_ip_table(reach_ip, unreach_ip):
    reach_ip = ["Reachable"] + reach_ip
    unreach_ip = ["Unreachable"] + unreach_ip
    longest = len(max(reach_ip, unreach_ip))
    shortest = len(min(reach_ip, unreach_ip))
    short_list = reach_ip if len(reach_ip) != longest else unreach_ip
    short_list = short_list.extend([""] * (longest - shortest))

    for row in zip(reach_ip, unreach_ip):
        print("{:15}{:15}".format(*row))
 