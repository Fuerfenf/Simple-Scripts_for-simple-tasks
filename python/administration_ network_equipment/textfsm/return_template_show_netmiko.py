# -*- coding: utf-8 -*-
"""
Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
"""
from itertools import repeat
import yaml
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
import clitable


def send_command(device, command):
    data = list()
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        data.append(result)
    return data


def send_show_command_to_devices(device, command, limit=3):
    data = list()
    with ThreadPoolExecutor(max_workers=limit) as worker:
        result = worker.map(send_command, [device, ], repeat(command))
    for device, items in zip(device, result):
        data.extend(items)
    return data


def send_and_parse_show_command(device_dict, command, templates_path, index="index"):
    out_list = list()
    attribut_dict = {
        'Command': command,
        'Vendor': "cisco_ios"
    }
    comm_out = send_show_command_to_devices(device_dict, command)
    cli_table = clitable.CliTable(index, templates_path)
    cli_table.ParseCmd(comm_out[0], attribut_dict)
    for itm in cli_table[1:]:
        out_list.append(dict(zip(cli_table[0], itm)))
    return out_list


if __name__ == "__main__":
    command = "sh ip int br"
    template_path = "templates"
    with open("devices.yaml") as f:
        device_list = yaml.safe_load(f)
    send_and_parse_show_command(device_list[0], command, template_path)

#alternative
def send_and_parse_show_command(device_dict, command, templates_path):
    if "NET_TEXTFSM" not in os.environ:
        os.environ["NET_TEXTFSM"] = templates_path
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command, use_textfsm=True)
    return output


if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), "templates")
    with open("devices.yaml") as f:
        devices = yaml.load(f, Loader=yaml.FullLoader)
    for dev in devices:
        result = send_and_parse_show_command(
            dev, "sh ip int br", templates_path=full_pth
        )
        pprint(result, width=120)

# without use_textfsm in netmiko
from task_22_3 import parse_command_dynamic


def send_and_parse_show_command(device_dict, command, templates_path):
    attributes = {"Command": command, "Vendor": device_dict["device_type"]}
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
        parsed_data = parse_command_dynamic(
            output, attributes, templ_path=templates_path
        )
    return parsed_data


if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), "templates")
    with open("devices.yaml") as f:
        devices = yaml.load(f, Loader=yaml.FullLoader)
    for dev in devices:
        result = send_and_parse_show_command(
            dev, "sh ip int br", templates_path=full_pth
        )
        pprint(result, width=120)

