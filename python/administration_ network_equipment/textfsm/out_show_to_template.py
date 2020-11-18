# -*- coding: utf-8 -*-
"""
parse_command_output. params:
* template - file name with template TextFSM (templates/sh_ip_int_br.template)
* command_output - output command show (строка)
f return:
* first elem - col names
* other - lists output changes
output/sh_ip_int_br.txt and templates/sh_ip_int_br.template.

2 var return dict lists
"""
import textfsm

def parse_command_output(template, command_output):
    out_list = list()
    with open(template) as templ:
        fsm = textfsm.TextFSM(templ)
        result = fsm.ParseText(command_output)
    out_list.append(fsm.header)
    out_list.extend([itm for itm in result])
    return out_list

if __name__ == "__main__":
    template = "templates/sh_ip_int_br.template"
    with open("output/sh_ip_int_br.txt", "r") as file:
        com_out = file.read()
    parse_command_output(template, com_out)

# refactor
def parse_command_output(template, command_output):
    with open(template) as tmpl:
        parser = textfsm.TextFSM(tmpl)
        header = parser.header
        result = parser.ParseText(command_output)
    return [header] + result


if __name__ == "__main__":
    with open("output/sh_ip_int_br.txt") as show:
        output = show.read()
    result = parse_command_output("templates/sh_ip_int_br.template", output)
    print(result)


#---------------------------------------------------------------------------------------------

# return dict lists
def parse_output_to_dict(template, command_output):
    out_list = list()
    with open(template) as templ:
        fsm = textfsm.TextFSM(templ)
        result = fsm.ParseText(command_output)
        headers = fsm.header

    for itm in result:
        out_list.append(dict(zip(headers, itm)))

    return out_list

if __name__ == "__main__":
    template = "templates/sh_ip_int_br.template"
    with open("output/sh_ip_int_br.txt", "r") as file:
        com_out = file.read()
    parse_output_to_dict(template, com_out)
    
 # alternative
 def parse_output_to_dict(template, command_output):
    with open(template) as tmpl:
        parser = textfsm.TextFSM(tmpl)
        header = parser.header
        result = parser.ParseText(command_output)
    return [dict(zip(parser.header, line)) for line in result]

if __name__ == "__main__":
    with open("output/sh_ip_int_br.txt") as show:
        output = show.read()
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    pprint(result, width=100)
    
#---------------------------------------------------------------------------------------------
 """
template return:
* mac - такого вида 00:04:A3:3E:5B:69
* ip - такого вида 10.1.10.6
* vlan - 10
* intf - FastEthernet0/10
file
output/sh_ip_dhcp_snooping.txt
"""
if __name__ == "__main__":
    template = "templates/sh_ip_dhcp_snooping.template"
    with open("output/sh_ip_dhcp_snooping.txt", "r") as file:
        com_out = file.read()
    parse_command_output(template, com_out)

