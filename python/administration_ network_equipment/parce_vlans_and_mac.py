# -*- coding: utf-8 -*-



"""
return list of matching vlans from 2 lists of vlans 
"""
command1 = "switchport trunk allowed vlan 1,2,3,5,8"
command2 = "switchport trunk allowed vlan 1,3,8,9"
list_command1_vlans = command1.split()[-1].split(',')
list_command2_vlans = command2.split()[-1].split(',')
intersection_vlans = sorted(set(list_command1_vlans) & set(list_command2_vlans))

#------------------------------------------------------------------------------------------------------

"""
return list vlans from port
"""
config = "switchport trunk allowed vlan 1,3,10,20,30,100"
list_vlan = config.split(' ')[-1].split(',')

#------------------------------------------------------------------------------------------------------

"""
return parced info about OSPF protocol as:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0
with file 
"""
line = """
Protocol:              {}
Prefix:                {}
AD/Metric:             {}
Next-Hop:              {}
Last update:           {}
Outbound Interface     {}
"""
output = "\n{:25} {}" * 6
with open("ospf.txt", "r") as f:
    for line in f:
        route = line.replace(",", " ").replace("[", "").replace("]", "")
        _, prefix, ad_metric, _, nhop, update, intf = route.split()

        print(output.format(
            "Protocol:", "OSPF",
            "Prefix:", prefix,
            "AD/Metric:", ad_metric,
            "Next-Hop:", nhop,
            "Last update:", update,
            "Outbound Interface:", intf,
        ))

#------------------------------------------------------------------------------------------------------


"""
return mac in binary
"""
mac = "AAAA:BBBB:CCCC"
bin_mac = "{:b}".format(int(mac.replace(":", ""), 16))
"""
return mac in binary examle 10.1.1.1:
10        1         1         1
00001010  00000001  00000001  00000001
"""
output = """
{0:<10}{1:<10}{2:<10}{3:<10}
{0:08b}  {1:08b}  {2:08b}  {3:08b}"""
ip = "192.168.3.1"
octets = ip.split(".")
print(output.format(int(octets[0]), int(octets[1]), int(octets[2]), int(octets[3])))
#------------------------------------------------------------------------------------------------------