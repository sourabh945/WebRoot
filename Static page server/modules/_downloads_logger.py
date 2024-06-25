from csv import writer as wr
from datetime import datetime as dt
 
#############################################

from modules.error_logger import error_log # this function create the logs of errors in ./logs/error_logs.csv file

#############################################
"""
download_log(user:users_module.user,filename:str):
It is function that create the logs of the files downloaded by users
with its download time, users ipaddress and the session_id  and return the bool
as the status for log is logged or not.
"""
def downloads_logger(user:object,filename:str) -> bool:
    try:
        with open("./logs/user_downloads_logs.csv","a") as file:
            writer = wr(file)
            writer.writerow([user.username,user.ipaddress,user.session_id,filename,dt.now()])
        return True
    except Exception as error:
        error_log(error,downloads_logger)
        return False 