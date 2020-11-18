# -*- coding: utf-8 -*-
"""
parse_command_dynamic.
params:
* command_output - command out line
* attributes_dict - atrr wuth :
 * 'Command': command
 * 'Vendor': vendor
* index_file - file name, connection between commands and templates. default = "index"
* templ_path - catalog with templates. default - templates

return dict list:
* key - name in  TextFSM
* value - output parts 
used command =  sh ip int br.
"""

import clitable

def parse_command_dynamic(command_output, attributes_dict, index_file="index", templ_path="templates"):
    out_list = list()
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    for itm in cli_table[1:]:
        out_list.append(dict(zip(cli_table[0], itm)))
    return out_list

if __name__ == "__main__":
    command = "sh ip int br"
    attribut_dict = {
        'Command': command,
        'Vendor': "cisco_ios"
    }

    with open('output/sh_ip_int_br.txt', 'r') as file:
        comm = file.read()
    parse_command_dynamic(comm, attribut_dict)
    
#refactor
def parse_command_dynamic(
    command_output, attributes_dict, index_file="index", templ_path="templates"
):
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    return [dict(zip(cli_table.header, row)) for row in cli_table]


if __name__ == "__main__":
    attributes = {"Command": "show ip int br", "Vendor": "cisco_ios"}
    with open("output/sh_ip_int_br.txt") as f:
        command_output = f.read()
    result = parse_command_dynamic(command_output, attributes)
    pprint(result, width=100)