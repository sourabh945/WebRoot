import os 

###########################

### This function is user to log any occur during the process
from modules.error_logger import error_log 

#############################################3

### This function is heart for the security it is function that detect the user have
### permission to access the directory or a file

def path_validator(selected_folder_path:str,folder_path:str) -> bool:
    try:
        parent_path_list = selected_folder_path.split("/")
        daughter_path_list = folder_path.split("/")
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
        path_list = path.split("/")
        res = path_list[0]
        for i in range(1,len(path_list-1)):
            res = res + "/" + path_list[i]
        return path+"/"
    except Exception as error:
        error_log(error,parent_path)
        return path
    
###############################################

### this function take path of file and separate it into folder_path and filename
def path_separator(file_path:str) -> tuple[str,str]:
    try:
        path_list = file_path.split("/")
        res = path_list[0]
        for i in range(1,len(path_list-1)):
            res = res + "/" + path_list[i]
        return res+"/" , path_list[-1]
    except Exception as error:
        error_log(error,path_separator)
        return file_path
