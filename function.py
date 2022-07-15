import os
import glob
from datetime import datetime

date = datetime.now()
root_path = os.path.dirname(os.path.abspath(__file__))

def log(msg=None,count=None):
    with open(root_path+"/error.txt", 'a+') as err:
        err.seek(0)
        data = err.read(100)

        if len(data) > 0:
            err.write("\n")
                
        err.write(f"{date} - Line: {count}, Message: {msg}.")

def fileCleanUp(path,file_name=None,file_ext=None):
    file = None
    files = 0

    if (file_name == None and file_ext != None ):
        file = os.path.join(root_path,path,'*'+file_ext)
        files = glob.glob(file)
    else:
        file = os.path.join(root_path,path,file_name+file_ext)
    print(file)
    try:
        if len(files) > 0:
            for file_path in files:
                os.remove(file_path)
        else:
            os.remove(file)
    except Exception as err:
        log(msg=err)
        print(err)

def jobs():
    fileCleanUp('providerFiles',None,'.pdf')
