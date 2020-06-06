# Made by @inoffensivo on Telegram.

import os, zipfile, time

# VARS
start = time.time()
DIR = os.getcwd()
files_count = 0

# NOME DEL FILE
backup_file = 'backup.zip'
# CARTELLE DA SALVARE
dirs = ['/root','/var/www', '/home', '/usr/local/sbin', '/etc/systemd/system']
# FILE DA ESCLUDERE (DOVETE LASCIARE IL PRIMO, PER EVITARE CHE SI AUTO-BACKUPI IL FILE DI BACKUP)
exclude_files = [DIR + '/' + backup_file]

# FUNCTIONS
def getListOfFiles(path):
    listOfFile = os.listdir(path)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(path, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def clearBackup():
    global DIR
    global backup_file
    if os.path.exists(DIR + '/' + backup_file):
        os.remove(DIR + '/' + backup_file)
        with zipfile.ZipFile(backup_file, "w") as zip:
            zip.close()
    return True

def createBackup():
    if clearBackup():
        global dirs
        global files_count
        with zipfile.ZipFile(backup_file, "a") as zip:
            for x in dirs:
                dirs_files = getListOfFiles(x)
                for i in dirs_files:
                    if not i in exclude_files:
                        files_count += 1
                        zip.write(i)
                        if files_count%100 == 0:
                            os.system('clear')
                            print(f"#####################\n# BACKUP IN CORSO..\n# FILE SALVATI: {files_count}\n#####################")
            zip.close()

        return dirs, files_count
    else:
        return False, False


# PROGRAM
dirs, files_count = createBackup()
os.system('clear')
if files_count != False and dirs != False:
    end = time.time()
    seconds = round(end-start,2)
    print(f"""#####################
# BACKUP COMPLETATO
#
# Tempo: {str(seconds)}s
# Numero Files: {files_count}
# File: {DIR + '/' + backup_file}
#
# by @inoffensivo
#####################
    """)
else:
    print('WTF')
