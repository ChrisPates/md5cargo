#!/usr/bin/python

import os

dirDatasets = "./datasets"
dirDB = "./dbs"
dirSQL = dirDB + "/sql"
dirSnapshots = "./snapshots"

print("Removing Databases:")

for the_file in os.listdir(dirDB):
    file_path = os.path.join(dirDB, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception, e:
        print e

print("Removing sql scripts:")
for the_file in os.listdir(dirSQL):
    file_path = os.path.join(dirSQL, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception, e:
        print e

