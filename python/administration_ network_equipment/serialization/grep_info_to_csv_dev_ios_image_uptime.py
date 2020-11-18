# -*- coding: utf-8 -*-
"""
main info:
* take info from sh version
* parce it and take info about devices
* write info to csv file
function parse_sh_version:
* оarg- line  sh version parce reg it
* return tuple:
 * ios -  "12.4(5)T"
 * image -  "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime -  "5 days, 3 hours, 3 minutes"
Function write_inventory_to_csv take two args:
 * data_filenames - list files with outline sh version
 * csv_filename - file name ( routers_inventory.csv), for write CSV
* treatment info from all files contented sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* with parse_sh_version, from all outputs grep info ios, image, uptime
* from file name grep device type
* write csv
Output file routers_inventory.csv content:
* hostname, ios, image, uptime
"""
import re
import glob
import csv

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]


def parse_sh_version(data_version):

    re_ios = "(Version\s+.{10})"
    ios_cach = re.search(re_ios, data_version).group()
    ios = ios_cach.split(" ")[1].replace(',', '')
    re_image = "(System image file is)\s+(?P<image>\S+)"
    image_cach = re.search(re_image, data_version)["image"].replace('\"', "")
    re_uptime = "(router uptime is)\s+(?P<uptime>\d*\s+days,\s+\d*\s+hours,\s+\d*\s+minutes)"
    re_uptime = re.search(re_uptime, data_version)["uptime"]

    return ios, image_cach, re_uptime


def write_inventory_to_csv(data_filenames, csv_filename):

    data_to_file = []
    data_to_file.append(headers)

    for file_name in data_filenames:
        with open(file_name, "r") as file:
            device = [file_name.split("_")[-1].split('.')[0], ]
            file_data = file.read()
            sh_data = parse_sh_version(file_data)
            device.extend(sh_data)
            data_to_file.append(device)
    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        for row in data_to_file:
            writer.writerow(row)

write_inventory_to_csv(sh_version_files, "routers_inventory.csv")

# other var
def parse_sh_version(sh_ver_output):
    match = re.search(
        "Cisco IOS .*? Version (?P<ios>\S+), .*"
        "uptime is (?P<uptime>[\w, ]+)\n.*"
        'image file is "(?P<image>\S+)".*',
        sh_ver_output,
        re.DOTALL,
    )
    if match:
        return match.group("ios", "image", "uptime")
    return (None, None, None)


def write_inventory_to_csv(data_filenames, csv_filename):
    headers = ["hostname", "ios", "image", "uptime"]
    with open(csv_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for filename in data_filenames:
            hostname = re.search("sh_version_(\S+).txt", filename).group(1)
            with open(filename) as f:
                parsed_data = parse_sh_version(f.read())
                writer.writerow([hostname] + list(parsed_data))


if __name__ == "__main__":
    sh_version_files = glob.glob("sh_vers*")
    write_inventory_to_csv(sh_version_files, "routers_inventory.csv")