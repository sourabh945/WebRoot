import os 
from flask import abort

###########################

### This function is user to log any occur during the process
from modules.error_logger import error_log , other_error_logger
from modules.folder_selector import sharing_folder_path
from _paths import _separator

#############################################

### This function is heart for the security it is function that detect the user have
### permission to access the directory or a file

def path_validator(folder_path:str) -> bool:
    try:
        parent_path_list = sharing_folder_path.split(_separator)
        daughter_path_list = folder_path.split(_separator)
        if len(parent_path_list) > len(daughter_path_list):
            return False
        else:
            for i in range(0,len(parent_path_list)):
                if parent_path_list[i] != daughter_path_list[i]:
                    return False
            return True
    except Exception as error:
        error_log(error,path_validator)
        return False
    
################################################

### This function return the parent_folder_path for a given path
def parent_path(path:str) -> str:
    try:
        path_list = path.split(_separator)
        res = path_list[0]
        for i in range(1,len(path_list)-1):
            res = res + _separator + path_list[i]
        return res
    except Exception as error:
        error_log(error,parent_path)
        return path 
    
###############################################

### this function take path of file and separate it into folder_path and filename
def path_separator(file_path:str) -> tuple[str,str]:
    try:
        path_list = file_path.split(_separator)
        res = path_list[0]
        for i in range(1,len(path_list)-1):
            res = res + _separator + path_list[i]
        return res+_separator , path_list[-1]
    except Exception as error:
        error_log(error,path_separator)
        return file_path , file_path
    
#######################################################

### This function take path of a file that user wanted to upload it verify that this file
### is exist or not if it not exist then user can upload file but if it exists then it return 
### a new file name with numeric index after it.

def upload_path_validator(folder_path:str,filename:str) -> str:
    try:
        if path_validator(folder_path) is True:
            files = set(os.listdir(folder_path))
            if filename not in files:
                return os.path.join(folder_path,filename)
            else:
                _name , _extension = os.path.splitext(filename)[0] , os.path.splitext(filename)[1]
                i = 1 
                _filename = f'{_name}({i}){_extension}'
                while _filename in set(os.listdir(folder_path)):
                    i = i + 1 
                    _filename = f'{_name}({i}){_extension}'
                return _filename
        else:
            other_error_logger("Path Validation Error","Upload are happening to a invalid path where share is not allowed",upload_path_validator)
            abort(500)
    except Exception as error:
        error_log(error,upload_path_validator)
        abort(500)