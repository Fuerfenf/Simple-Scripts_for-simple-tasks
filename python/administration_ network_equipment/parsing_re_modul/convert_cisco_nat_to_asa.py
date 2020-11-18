# -*- coding: utf-8 -*-
"""
function convert_ios_nat_to_asa, convert rules NAT from syntax cisco IOS to cisco ASA.

take two args:
- file name with rules NAT Cisco IOS
- out file NAT for ASA
file test cisco_nat_config.txt.

examples NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

converted NAT for ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023
interfaces are same for inside/outside
"""
import re

# old 
def convert_ios_nat_to_asa(file_nat_cisco, file_nat_asa):
    out_command_list = []
    format_command = ['object network LOCAL_{ip}\n',
                     ' host {ip}\n',
                     ' nat (inside,outside) static interface service tcp {oport} {iport}\n']
    with open(file_nat_cisco, "r") as file:
        regular_actet = """(?P<ip>\S+\d+\.\d+\.\d+\.\d+)\s+(?P<oport>\d+)\s+\w+\s+\w+\/\w+\s+(?P<iport>\d+)"""
        for line in file:
            match = re.search(regular_actet, line)
            out_command_list.append(''.join(format_command).format(ip=match["ip"],
                                                                   oport=match["oport"],
                                                                   iport=match["iport"]))
    with open(file_nat_asa, "w+") as wfile:
        wfile.writelines(out_command_list)
convert_ios_nat_to_asa("cisco_nat_config.txt", "asa_coverted_nat_from_cisco.txt")

#refactored best
def convert_ios_nat_to_asa(cisco_ios, cisco_asa):
    regex = (
        "tcp (?P<local_ip>\S+) +(?P<lport>\d+) +interface +\S+ (?P<outside_port>\d+)"
    )
    asa_template = (
        "object network LOCAL_{local_ip}\n"
        " host {local_ip}\n"
        " nat (inside,outside) static interface service tcp {lport} {outside_port}\n"
    )
    with open(cisco_ios) as f, open(cisco_asa, "w") as asa_nat_cfg:
        data = re.finditer(regex, f.read())
        for match in data:
            asa_nat_cfg.write(asa_template.format(**match.groupdict()))


if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "cisco_asa_config.txt")