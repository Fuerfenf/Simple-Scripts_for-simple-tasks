__author__ = "Egor"
__date__ = "08.12.2018"
__description__ = "Log_file_achiever"

"""This program processes files received from server log. the beginning of
files begins with this type, example: 20180521- *. Of all the files 
remain in the log folder only those who are less than 3 months.
Those files that are from three months to 3 years old are archived,
the rest files over 3 years are deleted."""

import tarfile
import os
import datetime

# Initial data :
# Paths to directories where the log is and where to put the archive.
dir_log = "*:/*****/*****/****"  # write the full path to the log folder
dir_backup = "+:/++++++++++/++++++++++/+++++"  # write the full path to the backup folder
# The current date from the system.
date_now = datetime.datetime.now()
print("The program is running")
# List with names of files in directory (dir_log)
try:
    source_files = os.listdir(dir_log)
except:
    print("There are no files in the directory !")
for file in source_files:
    date_file_convert = datetime.datetime.strptime(str(file.split("-")[0]), "%Y%m%d")
    days = int((str(date_now - date_file_convert)).split(" ")[0])
    if 93 < days < 1098:
        name_arh = os.path.join(dir_backup + file[0:6] + ".tar.gz")
        with tarfile.open(name_arh, "w:gz") as tar:
            path_file = os.path.join(dir_log + file)
            if os.path.isfile(path_file):
                tar.add(path_file)
        tar.close()
        os.remove(os.path.join(dir_log + file))
    elif days > 1098:
        os.remove(os.path.join(dir_log + file))
    elif days < 0:
        print("Congratulations, you opened the way to the future, as these files "
              "in your universe have not yet been created.")
        print(file)
    else:
        unchanged = []
        unchanged.append(file)
print("Files within three months are left in the log folder unchanged.", len(unchanged))
print("The program has finished")
