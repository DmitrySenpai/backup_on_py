import os
import json
import sys
import shutil

with open('config.json') as json_file:
    json_setting = json.load(json_file)

path_save_backup = json_setting["path_save_backup"]

print("[Backup on Python]: Import Backup.\nVersion: 0.3 [Alpha]\n\n")
if (len(sys.argv) == 1):
    print("Please write the date which copy you want to import.\nFor example: 01.05.2020\n\nTo exit write: exit")
    sel = input(">")
else:
    sel = sys.argv[1]

if (sel == "exit"):
    sys.exit()

if (os.path.isdir(path_save_backup + "DATE\\" + sel) == False):
    print("There is no such backup!\nCheck if the date is correct. Or copy is not available for this period")
    sys.exit()

if (os.path.isdir("import\\" + sel) == False):
    os.mkdir("import\\" + sel)

with open(path_save_backup + "DATE\\" + sel + '\\files.json') as json_file:
    json_files = json.load(json_file)

for x in json_files:
    data_import = "import\\" + sel + "\\" + x
    if (os.path.isdir(data_import) == False):
        os.mkdir(data_import)
    for n in json_files[x]:
        shutil.copyfile(path_save_backup + "STORAGE_BACKUP\\" + json_files[x][n]['path_md5'] + "\\" + json_files[x][n]['md5'], data_import + "\\" + json_files[x][n]['name'])

print("\n\nThe files were successfully imported to: import\\" + sel + "\\")