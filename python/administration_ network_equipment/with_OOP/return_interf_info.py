# -*- coding: utf-8 -*-

"""
send_show_command:
In [4]: r1.send_show_command('sh ip int br', parse=False)
Out[4]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

In [5]: r1.send_show_command('sh ip int br', parse=True)
Out[5]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '190.16.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.100',
  'address': '10.100.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.200',
  'address': '10.200.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.300',
  'address': '10.30.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback0',
  'address': '10.1.1.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback55',
  'address': '5.5.5.5',
  'status': 'up',
  'protocol': 'up'}]
"""
import telnetlib
import time
import textfsm


class CiscoTelnet:

    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username:")
        self._write_line(username)
        self.telnet.read_until(b"Password:")
        self._write_line(password)
        if secret:
            self.telnet.write(b"enable\n")
            self.telnet.read_until(b"Password:")
            self._write_line(secret)
        time.sleep(0.5)
        self.telnet.read_very_eager()

    def _write_line(self, data):
        self.telnet.write(data.encode("ascii") + b"\n")

    def send_show_command(self, command,  templates="templates", parse=False):
        data = list()
        key_list = ["intf", "address", "status", "protocol"]
        self.telnet.write(command.encode("ascii") + b"\n")
        time.sleep(1)
        output_data = self.telnet.read_very_eager().decode("ascii")
        if "Invalid input detected" in output_data:
            raise ValueError("Ошибка Invalid input")
        if parse:
            with open(templates + "/sh_ip_int_br.template") as templ:
                fsm = textfsm.TextFSM(templ)
                output_statuses = fsm.ParseText(output_data)
            for itm in output_statuses:
                data.append(dict(zip(key_list, itm)))
            return data
        else:
            return output_data

    def close_session(self):
        self.telnet.close()


r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
}

r1 = CiscoTelnet(**r1_params)
print(r1.send_show_command("sh ip int br", parse=True))
r1.close_session()