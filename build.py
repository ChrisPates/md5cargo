#!/usr/bin/python

import os, shutil, re

# Paths
dirDatasets = "./datasets"
dirDB = "./dbs"
dirSnapshots = "./snapshots"


dirSQL = dirDB + "/sql/"
DBcreate = dirDB + "/templates/create.sql"
DBimport = dirDB + "/templates/import.sql"

# REGEX templates
#
#extracts dataset and timestamp from 'CARGO' file names
snapshotRegex = re.compile(r'(?P<snapshot>(?P<dataset>[0-9a-zA-Z]+)-(?P<timestamp>(?P<date>[0-9]+)T(?P<time>[0-9]+)Z)).md5')
#extracts timestamp elements from yyyymmddThhmmssZ style iso timestamps
timestampRegex = re.compile(r'(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})T(?P<hour>[0-9]{2})(?P<minute>[0-9]{2})(?P<second>[0-9]{2}).')

# Parse source tree to identify datasets
dirs = os.listdir( dirDatasets )
datasets = []

for file in dirs:
   if os.path.isdir(dirDatasets + "/" + file) :
      manifest = dirDatasets + "/" + file + "/manifests"	
      if os.path.exists(manifest) and os.path.isdir(manifest) and os.listdir(manifest):
	 datasets.append(file)

print("Identified the following valid datasets:")
print(datasets)


# Prepare output locations
if not os.path.exists(dirDB):
   os.mkdir(dirDB)
if not os.path.exists(dirSQL):
   os.mkdir(dirSQL)

print("Processing manifests")

for dataset in datasets:
   manifests = []
   print("Processing: " +  dataset)

   createDB = dirSQL + dataset + ".sql"
   if not os.path.exists(createDB):
      print("   Generating createDB script " + createDB)
      shutil.copyfile( DBcreate, createDB )
   else:
      print("   Keeping existing createDB script " + createDB)
      
   dirs = os.listdir( dirDatasets + "/" +  dataset + "/manifests/" )

   for file in dirs:
      # Parse the filename to extract dataset and timestamp
      snapshot = snapshotRegex.match(file)
#      print snapshot.group('snapshot', 'dataset','date','time', 'timestamp')

      # Generate output file path
      importDB = dirSQL + snapshot.group('snapshot') + ".sql"
      if 
      print("   Creating import wrapper for snapshot: " + importDB)

      #create ISO Format Time Stamp
      timestamp = timestampRegex.match(snapshot.group('timestamp'))
      
#      print(timestamp.group('year', 'month', 'day','hour', 'minute', 'second'))
      replacements = {
         'MANIFEST_FILE': dirDatasets + dataset + "/manifests/" + file,
         'MANIFEST_SNAPSHOT':snapshot.group('snapshot'),
         'MANIFEST_TIMESTAMP': timestamp.group('year') + "-" + timestamp.group('month') + "-" + timestamp.group('day') + "T" + timestamp.group('hour') + ":" + timestamp.group('minute') + ":" + timestamp.group('second')
         }

      with open(DBimport) as infile, open(importDB, 'w') as outfile:
         for line in infile:
            for src, target in replacements.iteritems():
               line = line.replace(src, target)
            outfile.write(line)
