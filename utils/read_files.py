import os

def listdirs(rootdir):
    rootdirs = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            listdirs(d)
            rootdirs.append(d)
    return rootdirs

def listfiles(rootdir):
    files = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)

        files.append(d)
    return files

def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words