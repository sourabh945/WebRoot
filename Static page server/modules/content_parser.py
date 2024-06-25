import os 

###########################

### This function is user to log any occur during the process
from modules.error_logger import error_log 

    
##############################################

### this function is list all the folder and file in the given folder path 
### it take folder_path as argument and return list of tuple of 
### folder/file name, type and size of file in string 

def content_of(folder_path:str) -> list[tuple[str,str,str]]:
    try:
        content = []
        index = os.listdir(folder_path)
        for i in index:
            size = (os.path.getsize(folder_path+"/"+i))/1024
            if size == 0:
                size_ = '0 B'
            elif size < 200 and size > 0:
                size_ = f'{round(size,3)} KB'
            elif size >= 200 and size < 800*1024:
                size = size/1024
                size_ = f'{round(size,2)} MB'
            else:
                size = size/(1024*1024)
                size_ = f'{round(size,3)} GB'
            if os.path.isdir(folder_path+"/"+i) is True:
                content.append((i,"dir",size_))
            else:
                content.append((i,'file',size_))
        return content
    except Exception as error:
        error_log(error,content_of)
        return []
    
#################################################