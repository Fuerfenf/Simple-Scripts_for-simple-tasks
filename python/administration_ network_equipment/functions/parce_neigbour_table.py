# -*- coding: utf-8 -*-
'''
function parse_cdp_neighbors, parce show cdp neighbors.
take 1 param - command_output, read in line and sent in function
return dict.
example:
R4>show cdp neighbors
Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0
return value:
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
file give in function sh_cdp_n_sw1.txt
'''
def pattern(command_line):
    if ">" in command_line:
        line = command_line.split(">")[0]
        main_device = [line.replace("\n", "") if "\n" in line else line][0]
    com_line = command_line.split("\n")
    point_slice = [com_line.index(itm) for itm in com_line if "Device ID" in itm][0]
    return main_device, com_line[point_slice+1:]


def parse_cdp_neighbors(command_output):
    parsed_data = dict()
    sorted_info = pattern(command_output)
    for itm_line in sorted_info[1]:
        if itm_line:
            device_port = [itm for itm in itm_line.split(" ") if itm]
            loc_int = "".join(device_port[1:3])
            port_id = "".join(device_port[-2:])
            parsed_data[(sorted_info[0], loc_int)] = (device_port[0], port_id)
    return parsed_data


def grep_lines(file_cmd_line):
    with open(file_cmd_line, "r") as file:
        return file.read()


com_line_out = grep_lines("sh_cdp_n_sw1.txt")
data = parse_cdp_neighbors(com_line_out)
print(data)

"""
alternative
"""
def parse_cdp_neighbors(command_output):
    result = {}
    for line in command_output.split("\n"):
        line = line.strip()
        if ">" in line:
            hostname = line.split(">")[0]
        elif line and line[-1].isdigit():
            r_host, l_int, l_int_num, *other, r_int, r_int_num = line.split()
            # other take other elements, with not explicit
            result[(hostname, l_int + l_int_num)] = (r_host, r_int + r_int_num)
    return result

if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt", "r") as show_in:
        print(parse_cdp_neighbors(show_in.read()))