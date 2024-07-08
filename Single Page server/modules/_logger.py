import os 
from datetime import datetime as dt

############## _paths imports ########################

from _paths import log_folder , error_log_file , user_logs

######################################################

from modules.user import user

#######################################################

### this function return the path of the func

def get_path(func) -> str:
    return f'{func.__code__.co_filename}' if type(func) == "<class 'function'>" else f'{func.__name__}'

### this function create the log file for error records

def create_error_file() -> None:

    if log_folder not in os.listdir(os.path.curdir):
        os.mkdir(log_folder)

    if error_log_file not in os.listdir(error_log_file):
        file = open(error_log_file,"w")
        file.close()


### this function is for log the error 

def log_error(error:Exception,instance) -> None:
    
    create_error_file()

    try:
        with open(error_log_file,'a') as file:
            file.writelines(["",f'[{dt.now()}] : Error : {error}',f'\t Cause : {error.__cause__}  [function] : {get_path(instance)}',""])
    except:
        raise Exception
    
    print('\n >>>>>>>>>>>>>>    ERROR   >>>>>>>>>>>>>>>\n')
    print(f'Error: {error}\n Cause: {error.__cause__}\n Traceback: {error.__traceback__.tb_frame.f_back}\n Function_path: {get_path(instance)}')
    print('\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')


############################################################

### this logged the user when they login 

def log_user(user:user) -> bool:
    try:
        with open(user_logs,'a') as file:
            file.writelines["",f"[{dt.fromisoformat(user.time_of_login)}] [{user.session_id}] {user.username} {user.ip_address} ",""]
            file.close()
        return True
    except Exception as error:
        log_error(error,log_user)
        return False