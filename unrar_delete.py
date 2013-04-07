#!/usr/bin/env python3
""" Recursively searches for rar files, extracts them, and then deletes the source files """

# Copyright (C) 2012 - Jack Culhane

import os
import fnmatch
import glob
import re

FileCheckRE = re.compile('^(\w*?)(\d+)$')

def extractfile(root, filename):
    """ Extracts the filename in root to root, if successful will delete the source files """

    filepath = os.path.join(root, filename)

    if not os.path.exists(filepath):
        return
    
    print('Extracting "' + filepath + '"')

    res = os.system('unrar x "' + filepath + '" "' + root + '"')

    if res == 0:
        print('Deleting source files')
        delRarFiles(root, filename)
    else:
        print('Error', res, 'occurred during extraction, will not delete source files')


def delRarFiles(root, filename):
    """ Deletes filename.rar and and filename.r## files in root """
    
    FilePattern = None
    FilePrefix = None
    fileparts = filename.split('.')

    if len(fileparts) > 2:
        print(fileparts[-2])
        Match = FileCheckRE.match(fileparts[-2])
        if Match is not None:

            print("matched")

            PartPrefix = Match.group(1)
            print(PartPrefix)
            PartIndexLen = len(Match.group(2))
            FilePattern = '.' + PartPrefix + ('[0-9]'*PartIndexLen) + '.rar'
            
            FilePrefix = '.'.join(fileparts[:-2])

    if FilePattern is None: 
        FilePattern = '.r[0-9][0-9]'
        FilePrefix = os.path.splitext(filename)[0]
    
    # This is pointless, leaving it here in case I add a check above
    if FilePattern is None:
        print("Unable to determine naming convention, not deleting files")
        return
    
    print(FilePattern)

    globDir = os.path.join(root, FilePrefix).replace('[', '[[]') + FilePattern

    print(globDir)

    os.remove(os.path.join(root, filename))

    for file in glob.glob(globDir):
        print(file)
        os.remove(file)
        

if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for filename in fnmatch.filter(files, '*.rar'):
            extractfile(root, filename)


