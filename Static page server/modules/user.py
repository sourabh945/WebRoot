
from datetime import datetime as dt
from random import choices
from string import ascii_letters,digits
from csv import writer as wr

### Import form modules folder ###

from modules.error_logger import error_log ## function for log the error logs in ./logs/error_logs.csv file

######################################

# re_login_time : is time after the use have to re-login to access the files
re_login_time = 1; # time in hours

#####################################

### class users_modules contain all the necessary modules we use with user class to define user

class users_module:

    session_ids = {} ### this set contain all session ids that active in application
    
    logged_user = {} ### this set contain all users object that logged in application 

    ### and all users and its session id should to be in these sets because it use to authenticate user

    ###this function generate a unique session id to every logged user and this is complete random
    def id_generator(num:int=15):


    ### the class user is class to declare user it will generate user_login_logs, logout the user and validate user
    ### user need username and ipaddress for declare user 
    class user:
        def __init__(self,username,ipaddress) -> None:
            self.username = username
            self.ipaddress = ipaddress