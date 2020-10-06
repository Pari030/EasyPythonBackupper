import os
import zipfile
import time

# VARS
start = time.time()
DIR = os.getcwd()
files_count = 0

# File Name
backup_file = f'backup_{time.strftime("%d-%m-%Y"}.zip'

# Save Dirs
dirs = ['/root','/var/www', '/home']

# Excluded files (the first is the backuped file)
exclude_files = [DIR + '/' + backup_file]

# Get All Files 
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

# Delete Old Backup
def clearBackup():
    global DIR
    global backup_file
    if os.path.exists(DIR + '/' + backup_file):
        os.remove(DIR + '/' + backup_file)
        with zipfile.ZipFile(backup_file, "w") as zip:
            zip.close()
    return True

# Create Backup
def createBackup():
    if clearBackup():
        global dirs
        global files_count
        with zipfile.ZipFile(backup_file, "a") as zip:
            for x in dirs:
                dirs_files = getListOfFiles(x)
                for i in dirs_files:
                    if not i in exclude_files:
                        try:
                            zip.write(i)
                            files_count += 1
                        except:
                            pass
                        if files_count % 100 == 0:
                            os.system('clear')
                            print(f"#####################\n# BACKUP IN CORSO..\n# FILE SALVATI: {files_count}\n#####################")
            zip.close()

        return dirs, files_count
    else:
        return False, False


if __name__ == '__main__':
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
