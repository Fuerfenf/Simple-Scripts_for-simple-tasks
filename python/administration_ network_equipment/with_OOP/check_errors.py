# -*- coding: utf-8 -*-

"""


MyNetmiko(CiscoIosBase) from netmiko.

 __init__ in MyNetmiko connsect SSH  enable.



check MyNetmiko reachable send_command и send_config_set

In [2]: from task_27_2 import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '


 _check_error_in_command, errors:
 * Invalid input detected, Incomplete command, Ambiguous command

In [2]: from task_27_2a import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip br')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-1c60b31812fd> in <module>()
----> 1 r1.send_command('sh ip br')
...

"""

import netmiko
from netmiko.cisco.cisco_ios import CiscoIosBase


class ErrorInCommand(Exception):
    pass


class MyNetmiko(CiscoIosBase):

    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.ssh = netmiko.ConnectHandler(**device_params)
        self.ssh.enable()
        self.ip = device_params["ip"]

    def send_command(
        self,
        command_string,
        expect_string=None,
        delay_factor=1,
        max_loops=500,
        auto_find_prompt=True,
        strip_prompt=True,
        strip_command=True,
        normalize=True,
        use_textfsm=False,
        use_genie=False,
    ):
        result = super().send_command(command_string)
        self._check_errors_in_command(result, command_string)

    def _check_errors_in_command(self, result, command):
        errors = ["Invalid input detected", "Incomplete command", "Ambiguous command"]
        pattern = "При выполнении команды \"{}\" на устройстве {} возникла ошибка \"{}\""
        flag = [itm for itm in errors if itm in result]
        if flag:
            out = pattern.format(command, self.ip, result.replace("\n", ""))
            raise ErrorInCommand(out)


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

test = MyNetmiko(**device_params)
test.send_command("sh ip int br")

#alternative
class ErrorInCommand(Exception):
    """Exception wen run command"""


class MyNetmiko(CiscoIosBase):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()

    def _check_error_in_command(self, command, result):
        regex = "% (?P<err>.+)"
        message = (
            'При выполнении команды "{cmd}" на устройстве {device} '
            'возникла ошибка "{error}"'
        )
        error_in_cmd = re.search(regex, result)
        if error_in_cmd:
            raise ErrorInCommand(
                message.format(
                    cmd=command, device=self.ip, error=error_in_cmd.group("err")
                )
            )

    def send_command(self, command, *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, command_output)
        return command_output