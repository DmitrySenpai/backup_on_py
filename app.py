import os
import datetime
import time
import hashlib
import shutil
import json
from distutils.dir_util import copy_tree

with open('config.json') as json_file:
    json_setting = json.load(json_file)

path_save_backup = json_setting["path_save_backup"]
path_import_files = json_setting["path_import_files"]
count_backup_day = json_setting["count_backup_day"]

def check_term(x1, dir_sel, count_backup_day):

    x2 = datetime.datetime.strptime(dir_sel, '%d.%m.%Y')
    x1 = datetime.datetime.strptime(x1, '%d.%m.%Y')

    f_date = datetime.date(int(x1.year), int(x1.month), int(x1.day))
    l_date = datetime.date(int(x2.year), int(x2.month), int(x2.day))
    delta = f_date - l_date

    if (delta.days > count_backup_day):
        return(1)
    else:
        return(0)

def md5_files(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def list_files(startpath):
    dir_all = {}
    for root, dirs, files in os.walk(startpath):
        path_files = root.replace(startpath , '\\')
        #path_files = root + "\\"
        if (len(files) != 0):
            files_md5 = {}
            for x in files:
                path_full = root + "\\" + x
                md5_files_d = md5_files(path_full)
                files_md5.update({x: {'name': x, 'md5': hashlib.md5(str(x+md5_files_d).encode()).hexdigest(),'name_md5': hashlib.md5(x.encode()).hexdigest(), 'path_md5': hashlib.md5(path_files.encode()).hexdigest(), 'files_md5': md5_files_d}})
        dir_all.update({path_files: files_md5})
    return dir_all

def is_empty_array(array, index):
    try:
        array.index(index)
        return(True)
    except ValueError:
        return(False)

STORAGE_BACKUP = path_save_backup + "STORAGE_BACKUP\\"
path_save_backup = path_save_backup + "DATE\\"

print("[Backup on Python]: Service started!")
print("Version: 0.3 [Alpha]")
while True:
    time.sleep(260)
    while True:
        try:
            x = datetime.datetime.now()
            x1 = x.strftime("%d.%m.%Y")
            check_dir = os.listdir(path_save_backup).index(x1)
            break
        except ValueError:
            x = datetime.datetime.now()
            x1 = x.strftime("%d.%m.%Y")

            json_all = {}
            array_file_all_md5 = []

            os.mkdir(path_save_backup + x1)
            copy_tree(path_import_files, path_save_backup + x1 + "\\TEMP")
            
            #Create md5 json

            json_backup = list_files(path_import_files)

            with open(path_save_backup + x1 + "\\" + "files.json", "w") as outfile: 
                outfile.write(json.dumps(json_backup))


            for x in json_backup:
                #Select Path
                for n in json_backup[x]:
                    path_to_files = path_save_backup + x1 + "\\TEMP" + x + "\\"
                    os.rename(path_to_files + json_backup[x][n]['name'], path_to_files + json_backup[x][n]['md5'])

                    if(os.path.isdir(STORAGE_BACKUP + json_backup[x][n]['path_md5']) == False):
                        os.mkdir(STORAGE_BACKUP + json_backup[x][n]['path_md5'])
                    
                    if(os.path.isfile(STORAGE_BACKUP + json_backup[x][n]['path_md5'] + "\\" + json_backup[x][n]['md5']) == False):
                        shutil.move(path_to_files + json_backup[x][n]['md5'], STORAGE_BACKUP + json_backup[x][n]['path_md5'] + "\\" + json_backup[x][n]['md5'])
                    else:
                        os.remove(path_to_files + json_backup[x][n]['md5'])

            shutil.rmtree(path_save_backup + x1 + "\\TEMP")

            #Check
            for dir_sel in os.listdir(path_save_backup):
                if (check_term(x1, dir_sel, count_backup_day) == 1):
                    shutil.rmtree(path_save_backup + dir_sel)



            for dir_sel in os.listdir(path_save_backup):
                with open(path_save_backup + dir_sel + '\\files.json') as json_file:
                    json_files_all = json.load(json_file)
                json_all.update({dir_sel: json_files_all})

            for x3 in json_all:
                for x4 in json_all[x3]:
                    for x5 in json_all[x3][x4]:
                        if(is_empty_array(array_file_all_md5, json_all[x3][x4][x5]['path_md5'] + "\\" + json_all[x3][x4][x5]['md5']) == False):
                            array_file_all_md5.append(json_all[x3][x4][x5]['path_md5'] + "\\" + json_all[x3][x4][x5]['md5'])

            list_dir_storage = os.listdir(STORAGE_BACKUP)
            list_dir_storage_array = []
            for xx1 in list_dir_storage:
                list_dir_storage_sel = os.listdir(STORAGE_BACKUP + xx1)
                for xx2 in list_dir_storage_sel:
                    list_dir_storage_array.append(xx1 + "\\" + xx2)

            for xx3 in list_dir_storage_array:
                if (is_empty_array(array_file_all_md5, xx3) == False):
                    os.remove(STORAGE_BACKUP + xx3)

            break