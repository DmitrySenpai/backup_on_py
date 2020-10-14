import os
import datetime
import time
from distutils.dir_util import copy_tree

path_save_backup = ".\\BACKUP\\"
path_import_files = ".\\SIMPLE\\"
count_backup_day = 5

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
            os.mkdir(path_save_backup + x1)
            copy_tree(path_import_files, path_save_backup + x1)
            for dir_sel in os.listdir(path_save_backup):
                if (check_term(x1, dir_sel, count_backup_day) == 1):
                    os.rmdir(path_save_backup + dir_sel)
            break