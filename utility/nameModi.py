import os
currentPath = os.getcwd()

files=os.listdir(currentPath)

print(files)


for file in files:
    try:
        preFix, subFix = file.split('_')
        
        oldname=os.path.join(currentPath, file)
        newname=currentPath + '/' + preFix + '_F.log'
        os.rename(oldname,newname)
        print(oldname+'>>>'+newname)
    except:
        pass
