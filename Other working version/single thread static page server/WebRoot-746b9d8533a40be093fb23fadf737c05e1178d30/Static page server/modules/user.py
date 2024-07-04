
from datetime import datetime as dt
from random import choices
from string import ascii_letters,digits
from csv import writer as wr
from functools import wraps

### Import form modules folder ###

from modules.error_logger import error_log , other_error_logger## function for log the error logs in ./logs/error_logs.csv file

######################################

# re_login_time : is time after the use have to re-login to access the files
re_login_time = 1; # time in hours

###########################################################

### This a wrapper the verify that the object pass to any module of users_module has a object of class user_module.user
def object_validator(func):
    @wraps(func)
    def wrapper(obj):
        if type(obj).__name__ == 'user':
            return func(obj)
        else:
            other_error_logger("object error",'user object, that passed as argument is not of class user ',func)
        return False
    return wrapper

###########################################################

### class users_modules contain all the necessary modules we use with user class to define user

class users_module:

    session_ids = set() ### this set contain all session ids that active in application
    
    logged_users = {} ### this dict contain all users object that logged in application 

    ### logged_user = {username:str,user_module.user:object}

    ### and all users and its session id should to be in these sets because it use to authenticate user

    ########################################################

    ###this function generate a unique session id to every logged user and this is complete random

    def id_generator(num:int=32) -> str:
        res = "".join(choices(ascii_letters+digits,k=num))
        while res in users_module.session_ids:
            res = "".join(choices(ascii_letters+digits,k=num))
        return res
    
    ###########################################################

    ### the class user is class to declare user it will generate user_login_logs, logout the user and validate user
    ### user need username and ipaddress for declare user 
    """
    user:class(username,ipaddress)
    ------
    This is class to create user 
    """
    class user:

        ##########################################################

        ### This function create the user and this will also works as the login function 
        ### This add the user into the logged_users dict and session_id to session_ids set

        def __init__(self,username:str,ipaddress:str) -> None:
            self.username = username
            self.ipaddress = ipaddress
            self.session_id = users_module.id_generator(num=32)
            self.time_of_login = dt.now()
            if username in users_module.logged_users.keys():
                old_user_object = users_module.logged_users[username]
                old_user_object.logout()
            users_module.session_ids.add(self.session_id)
            users_module.logged_users[username] = self
            if users_module.user.user_logger(self,"login") is True:
                del self

        ###########################################################

        ### This function is for create log of user login or logouts and store them into
        ### file ./logs/user_logs.csv, and type is login or logout

        
        def user_logger(self,type:str) -> bool:
            try:
                with open("./logs/user_logs.csv","a") as file:
                    log_writer = wr(file)
                    if type=="login":
                        log_writer.writerow([self.username,self.ipaddress,self.session_id,self.time_of_login,"login"])
                    elif type=="logout":
                        log_writer.writerow([self.username,self.ipaddress,self.session_id,self.time_of_login,"logout",dt.now()])
                return True
            except Exception as error: 
                error_log(error,users_module.user.user_logger)
                return False
            
        ##########################################################

        ### This function delete the all instance of the user and after the authentication of 
        ### give false and it also delete from logged_users dict and session_ids set.

        
        def logout(self) -> bool:
            try:
                self.user_logger('logout')
                users_module.session_ids.remove(self.session_id)
                del users_module.logged_users[self.username]
                del self
                return True
            except Exception as error:
                error_log(error,users_module.user.logout)
                return False
            
        ##########################################################
            
        ### This function tell the user session is still valid or expired depending upon
        ### it return True or False as the return to function. It just check the user 
        ### into the logged_users and check the session_id in set sessions_ids.

        @object_validator
        def validate(self) -> bool:
            try:
                if (dt.now() - self.time_of_login).seconds > re_login_time*60*60:
                    self.logout()
                    return False
                else:
                    if self.session_id in users_module.session_ids and users_module.logged_users[self.username] == self:
                        return True
                    else:
                        return False
            except Exception as error:
                error_log(error,users_module.user.validate)
                return False
        #####################################################    

    #########################################################

#############################################################