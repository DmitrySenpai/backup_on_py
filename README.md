# Backup on Python

Before the first run, edit the "config.json" file:

```"path_save_backup": ".\\BACKUP\\",``` - Where to save copies

```"path_import_files": ".\\SIMPLE\\",``` - Where to copy files from

```"count_backup_day": 5``` - The maximum period of one backup. (Specified in days)

To import the backup, use this command:

```sh
python3 import.py
```

or

```sh
python3 import.py 21.10.2020(backup date)
```
