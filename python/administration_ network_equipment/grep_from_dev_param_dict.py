# -*- coding: utf-8 -*-
"""
grep from param dictionary if no key return no param
with input lower case
examle (ios, model, vendor, location, ip): IOS
15.4
"""
london_co = {
    "r1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.1",
    },
    "r2": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.2",
    },
    "sw1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "3850",
        "ios": "3.6.XE",
        "ip": "10.255.0.101",
        "vlans": "10,20,30",
        "routing": True,
    },
}
inp_device = london_co[(input("Input device name: ")).lower()]
list_items = ', '.join(inp_device.keys())
inp_param = (input("Input param name ({}): ".format(list_items))).lower()
out_data = inp_device.get(inp_param, "No such param")
print(out_data)
