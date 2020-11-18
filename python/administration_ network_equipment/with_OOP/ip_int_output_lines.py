# -*- coding: utf-8 -*-

"""
example:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from topology import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

"""


import telnetlib
import time


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

    def __enter__(self):
        return self

    def send_show_command(self, command):
        self.telnet.write(command.encode("ascii") + b"\n")
        time.sleep(1)
        output_data = self.telnet.read_very_eager().decode("ascii")
        if "Invalid input detected" in output_data:
            raise ValueError("Ошибка Invalid input")
        return output_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.telnet.close()


r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
}

with CiscoTelnet(**r1_params) as r1:
    print(r1.send_show_command("sh ip int br"))