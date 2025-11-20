import os
topPath = os.getcwd()
files = os.listdir(topPath)
files.remove('main.py')

print(files)
fileTypes = [name.split('.')[1] for name in files]
fileTypes = list(set(fileTypes))
for name in fileTypes:
    path = os.path.join(topPath,name)
    os.mkdir(path)

for fileName in files:
    src = os.path.join(topPath,fileName)
    dst = os.path.join(topPath,fileName.split('.')[1],fileName)
    os.rename(src,dst)