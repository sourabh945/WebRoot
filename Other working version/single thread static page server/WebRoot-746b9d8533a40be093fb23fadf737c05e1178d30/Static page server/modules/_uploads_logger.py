from csv import writer as wr
from datetime import datetime as dt
 
#############################################

from modules.error_logger import error_log # this function create the logs of errors in ./logs/error_logs.csv file
from _paths import _upload_log_file_path

#############################################
"""
upload_log(user:users_module.user,filename:str):
It is function that create the logs of the files uploads by users
with its uploads time, users ipaddress and the session_id  and return the bool
as the status for log is logged or not.
"""
def uploads_logger(user:object,filename:str) -> bool:
    try:
        with open(_upload_log_file_path,"a") as file:
            writer = wr(file)
            writer.writerow([user.username,user.ipaddress,user.session_id,filename,dt.now()])
        return True
    except Exception as error:
        error_log(error,uploads_logger)
        return False 