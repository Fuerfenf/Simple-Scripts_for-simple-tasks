# -*- coding: utf-8 -*-
"""
function send_config_commands
connect SSH (netmiko) to device run list of commands.

func args:
* device - dict with params
* config_commands - command list
* catch exeptions Invalid input detected, Incomplete command, Ambiguous command -> console log {command} {type exception} {device ip}

return out result command:
In [7]: r1
Out[7]:
{'device_type': 'cisco_ios',
 'ip': '192.168.100.1',
 'username': 'cisco',
 'password': 'cisco',
 'secret': 'cisco'}

In [8]: commands
Out[8]: ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']

In [9]: result = send_config_commands(r1, commands)

In [10]: result
Out[10]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#logging 10.255.255.1\nR1(config)#logging buffered 20010\nR1(config)#no logging console\nR1(config)#end\nR1#'

In [11]: print(result)
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.255.255.1
R1(config)#logging buffered 20010
R1(config)#no logging console
R1(config)#end
R1#
files wit device devices.yaml.

add break point if rejected command
Do next [y]/n:
* y - run commands
* n or no - break

send_config_commands return tuple two dicts with accepted and rejected commands:
dicts:
* key - command
* value - output run

example send_config_commands:
In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'a',
 'logging buffered 20010',
 'ip http server']
In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "a" выполнилась с ошибкой "Ambiguous command:  "a"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'a': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#a\n'
       '% Ambiguous command:  "a"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'a'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
"""
from netmiko import ConnectHandler
import yaml
import re

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]
commands = commands_with_errors + correct_commands

def send_config_commands(device, commands, log=True):
    with_error = dict()
    without_erros = dict()
    FLAG = True
    if log:
        print("Connection to {}".format(device["ip"]))
    with ConnectHandler(**device) as ssh:
        for command in commands:
            if FLAG:
                ssh.enable()
                config = ssh.config_mode()
                result = ssh.send_config_set(command)
                summary_out = config+result
                err = re.findall(r"(Invalid input detected|Incomplete command|Ambiguous command)", summary_out)
                if err:
                    print("Команда \"{}\" выполнилась c ошибкой {} на устройстве {}".format(command, err, device["ip"]))
                    user_ans = input("Продолжать выполнять команды? [y]/n:")
                    with_error[command] = summary_out
                    if user_ans == "n":
                        FLAG = False
                    else:
                        pass
                else:
                    without_erros[command] = summary_out
    return without_erros, with_error

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devise_list = yaml.safe_load(f)
    for dev_par in devise_list:
        if dev_par:
            send_config_commands(dev_par, commands)

            
# refactored
def send_config_commands(device, config_commands, verbose=True):
    good_commands = {}
    bad_commands = {}
    regex = "% (?P<errmsg>.+)"

    if verbose:
        print("Подключаюсь к {}...".format(device["ip"]))
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        for command in config_commands:
            result = ssh.send_config_set(command, exit_config_mode=False)
            error_in_result = re.search(regex, result)
            if error_in_result:
                message = 'Команда "{}" выполнилась с ошибкой "{}" на устройстве {}'
                print(message.format(command, error_in_result.group("errmsg"), ssh.ip))
                bad_commands[command] = result
                decision = input("Продолжать выполнять команды? [y]/n: ")
                if decision in ("n", "no"):
                    break
            else:
                good_commands[command] = result
            ssh.exit_config_mode()
    return good_commands, bad_commands


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        send_config_commands(dev, commands)