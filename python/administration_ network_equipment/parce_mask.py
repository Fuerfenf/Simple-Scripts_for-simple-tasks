# -*- coding: utf-8 -*-
"""
user input 10.1.1.0/24
input network and mask from run skript in console as argument
return as:
Network:
10        1         1         0
00001010  00000001  00000001  00000000
Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000
"""
from sys import argv

mask_dict_base = {
    "32": "255.255.255.255",
    "31": "255.255.255.254",
    "30": "255.255.255.252",
    "29": "255.255.255.248",
    "28": "255.255.255.240",
    "27": "255.255.255.224",
    "26": "255.255.255.192",
    "25": "255.255.255.128",
    "24": "255.255.255.0",
    "23": "255.255.254.0",
    "22": "255.255.252.0",
    "21": "255.255.248.0",
    "20": "255.255.240.0",
    "19": "255.255.224.0",
    "18": "255.255.192.0",
    "17": "255.255.128.0",
    "16": "255.255.0.0",
    "15": "255.254.0.0",
    "14": "255.252.0.0",
    "13": "255.248.0.0",
    "12": "255.240.0.0",
    "11": "255.224.0.0",
    "10": "255.192.0.0",
    "9": "255.128.0.0",
    "8": "255.0.0.0",
    "7": "254.0.0.0",
    "6": "252.0.0.0",
    "5": "248.0.0.0",
    "4": "240.0.0.0",
    "3": "224.0.0.0",
    "2": "192.0.0.0",
    "1": "128.0.0.0",
    "0": "0.0.0.0"}

# in_ip_mask = input("Введите IP-сети в вормате Network/CIDR_prefix : ")
in_ip_mask = argv[1]

list_ip_cidr = in_ip_mask.split("/")
ip = list_ip_cidr[0].split(".")
mask_list = mask_dict_base[list_ip_cidr[1]].split(".")

if 24 <= int(list_ip_cidr[1]) <= 32:
    rep = str(int(ip[3]) & int(mask_list[3]))
    ip[3] = rep
elif 16 <= int(list_ip_cidr[1]) <= 23:
    rep = str(int(ip[2]) & int(mask_list[2]))
    ip[2] = rep
    ip[3] = '0'
elif 8 <= int(list_ip_cidr[1]) <= 15:
    rep = str(int(ip[1]) & int(mask_list[1]))
    ip[1] = rep
    ip[2] = '0'
    ip[3] = '0'
elif 0 <= int(list_ip_cidr[1]) <= 7:
    rep = str(int(ip[0]) & int(mask_list[0]))
    ip[0] = rep
    ip[1] = '0'
    ip[2] = '0'
    ip[3] = '0'
else:
    print("CIDR_prefix incorrect.")

format_line = """
    Network:
    {a:<8} {b:<8} {c:<8} {d:<8}
    {a:08b} {b:08b} {c:08b} {d:08b}

    Mask:
    /{m}
    {a1:<8} {b1:<8} {c1:<8} {d1:<8}
    {a1:08b} {b1:08b} {c1:08b} {d1:08b}

"""
out = format_line.format(a=int(ip[0], 10), b=int(ip[1], 10), c=int(ip[2], 10), d=int(ip[3], 10),
                         m=list_ip_cidr[1],
                         a1=int(mask_list[0], 10), b1=int(mask_list[1], 10),
                         c1=int(mask_list[2], 10), d1=int(mask_list[3], 10))
                         
"""
alternative 
"""
network = input("Введите адрес сети: ")

ip, mask = network.split("/")
ip_list = ip.split(".")
mask = int(mask)

oct1, oct2, oct3, oct4 = [
    int(ip_list[0]),
    int(ip_list[1]),
    int(ip_list[2]),
    int(ip_list[3]),
]
bin_ip_str = "{:08b}{:08b}{:08b}{:08b}".format(oct1, oct2, oct3, oct4)
bin_network_str = bin_ip_str[:mask] + "0" * (32 - mask)

net1, net2, net3, net4 = [
    int(bin_network_str[0:8], 2),
    int(bin_network_str[8:16], 2),
    int(bin_network_str[16:24], 2),
    int(bin_network_str[24:32], 2),
]

bin_mask = "1" * mask + "0" * (32 - mask)
m1, m2, m3, m4 = [
    int(bin_mask[0:8], 2),
    int(bin_mask[8:16], 2),
    int(bin_mask[16:24], 2),
    int(bin_mask[24:32], 2),
]

ip_output = """
Network:
{0:<8}  {1:<8}  {2:<8}  {3:<8}
{0:08b}  {1:08b}  {2:08b}  {3:08b}"""

mask_output = """
Mask:
/{0}
{1:<8}  {2:<8}  {3:<8}  {4:<8}
{1:08b}  {2:08b}  {3:08b}  {4:08b}
"""
print(ip_output.format(net1, net2, net3, net4))
print(mask_output.format(mask, m1, m2, m3, m4))