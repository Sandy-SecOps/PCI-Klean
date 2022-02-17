import zipfile
import os

def unpack(target_files):
    zippedfiles=[]
    
    for x in target_files:
        print ('Checking if file: ' + x + ' is zip.')
        if x.endswith('.zip'):
            zippedfiles.append(x)
        else:
            print (x + ' does not have a zip extension.')
            
    if zippedfiles:
        target_files = [x for x in target_files if x not in zippedfiles]
        unzipped_files = unzip_action(zippedfiles)
        target_files.extend(unzipped_files)
        return(target_files)
    else:
        print ('There is no zipped files. Returning')
        return(target_files)
    
def unzip_action(target_files):
    for inputfile in target_files:
        filepath = os.path.dirname(os.path.abspath(inputfile))
        with zipfile.ZipFile(inputfile, 'r') as zipobj:
            unpackedfiles = zipobj.namelist()
            unpackedfiles = [filepath + '/' + i for i in unpackedfiles]
            zipobj.extractall(filepath)
    for x in unpackedfiles:
        if not os.path.isfile(x):
            print (x + ' - Was not extracted')
        else:
            print (x + ' - Was extracted correct.')
    return (unpackedfiles)

