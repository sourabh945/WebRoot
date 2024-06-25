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
    
