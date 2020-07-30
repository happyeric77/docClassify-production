import os

currentPath = os.getcwd()
files = os.listdir(currentPath)

input('-'*50+'\n{files} files in current folder will be renamed\nPress any key to start...'.format(files=len(files)))


renamedFiles = []
removedFiles = []

def check_exist(newname):
    if os.path.isfile(newname):
        try:
            os.remove(newname)
            print('file overlap --> {oldname} deleted'.format(oldname=file))
            removedFiles.append(file)
        except Exception as e:
            print('Fail to remove {file}: '.format(file=file) + e)

for file in files:
    print('--'*20 + '\nStart working on {file}\n'.format(file=file)+ '--'*20)
    oldname = os.path.join(currentPath, file)

    try:
        # Split file name by "_" symbol
        preFix, suffix = file.split('_')

        if suffix != 'F.log':
            newname = currentPath + '/' + preFix + '_F.log'

            # Check if file name overlap after rename
            check_exist(newname)
            # Rename file
            os.rename(oldname,newname)
            print(file +'>>>'+ preFix + '_F.log')
            renamedFiles.append(file)
    except:
        preFix, suffix = file.split('.')
        print(preFix, __file__)
        try:
            if (preFix+'.py') != __file__:
                newname = currentPath + '/' + preFix + '_F.log'
                check_exist(newname)
                os.rename(oldname, newname)
                print(file +'>>>'+ preFix + '_F.log')
                renamedFiles.append(file)
        except Exception as e:
            print('({file}) is not renamed and keep the name as it is\n'.format(file=file))
            print('detail: ' + str(e))

input('----'*20+'Total files in folder: {total}\nRenamed files: {rename}\nRemoved files: {remove}\n Press any key to finish process ...'.format(total=len(files), rename=len(renamedFiles), remove=len(removedFiles)))
