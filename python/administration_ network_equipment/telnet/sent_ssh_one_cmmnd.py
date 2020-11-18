# -*- coding: utf-8 -*-
"""
 function send_show_command.

connect SSH (netmiko) to one dev and sent command.

args:
* device - dict params for connect to device
* command - command to run on dev
* catch exceptions loggin fail
* catch exceptions unreacheble host
return line run com
devices devices.yaml 

"""
import yaml
import sys
from netmiko import (
    ConnectHandler,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)
command = "sh ip int br"

with open("devices.yaml") as f:
    devise_list = yaml.safe_load(f)

def send_show_command(device, command):

    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            return result
    except NetMikoAuthenticationException:
        print("Authentication failure: unable to connect")
    except NetMikoTimeoutException:
        print("Connection to device timed-out")


for dev_par in devise_list:
    print(send_show_command(dev_par, command))

# refactored
def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as error:
        print(error)


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    r1 = devices[0]
    result = send_show_command(r1, command)
    print(result)
