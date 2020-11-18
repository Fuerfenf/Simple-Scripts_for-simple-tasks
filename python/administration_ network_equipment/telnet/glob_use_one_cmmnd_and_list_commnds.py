# -*- coding: utf-8 -*-
"""
send_commands ( SSH , netmiko).

params:
* device - dict with params
* show - command show
* config - comand list

function  send_commands take, one of  show or config.

Далее комбинация из аргумента и соответствующей функции:
* show - send_show_command
* config - send_config_commands

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\nR1(config)#end\nR1#'
"""

from sent_ssh_one_cmmnd import send_show_command
from sent_ssh_commnds_list import send_config_commands
import yaml


commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
command = "sh ip int br"


def send_commands(device, config=None, show=None):

    if show:
        result_show = send_show_command(device, show)
        return result_show
    elif config:
        result_config = send_config_commands(device, config)
        return result_config
    elif config and show or config == show:
        return "INCORRECT INPUT PARAMETRS MUST BE ONE OF TWO PARAMETRS !"


if __name__ == "__main__":
    with open("devices.yaml") as f:
        device_list = yaml.safe_load(f)
    for device in device_list:
        send_commands(device, command)
        # send_commands(device, commands)
