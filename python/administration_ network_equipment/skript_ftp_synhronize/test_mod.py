import os
from ftplib import FTP
local_files = [] # create local dir list
remote_files = [] # create remote dir list
path = 'C:\\something\\bla\\' # local dir
ftp = FTP('ftp.server.com')
ftp.login('user', 'pass')

# read directory and write lists
if os.listdir(path) != []:
    print('Create local dir list:\n')
    for file_name in os.listdir(path):
        local_files.append(file_name) # populate local dir list
        ftp.sendcmd('CWD /directory.....')
        print('Create remote dir list:\n')
else:
    print('Report: Local dorectory is ampty')





for rfile in ftp.nlst():
    if rfile.endswith('.jpg'): # i need only .jpg files
        remote_files.append(rfile) # populate remote dir list

h_diff = sorted(list(set(remote_files) - set(local_files))) # difference between two list

for h in h_diff:
    with open(os.path.join(path,h), 'wb') as ftpfile:
        s = ftp.retrbinary('RETR ' + h, ftpfile.write) # retrieve file
    print('PROCESSING', h)
    if str(s).startswith('226'): # comes from ftp status: '226 Transfer complete.'
        print('OK\n') # print 'OK' if transfer was successful
    else:
        print(s) # if error, print retrbinary return
