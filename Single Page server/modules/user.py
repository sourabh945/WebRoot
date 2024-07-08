from datetime import datetime as dt
from random import choices
from string import ascii_letters , digits
from functools import wraps

from flask import abort

##################################################

from modules.var_client import sm_operator
from modules._logger import log_user , log_error

##################################################

re_login_time = 1 ### this the time after that user have to re login is required

##################################################

### decorator for validate the object pass is of user class

def object_validator(func):
    @wraps
    def wrapper(obj):
        if type(obj).__name__ == 'user':
            return func(obj)
        else:
            abort(500)
    return wrapper


### this function generate unique session when the use login

def id_generate(num=32):
    res = "".join(choices(ascii_letters+digits,k=num))
    __existing_session_ids = sm_operator('session_ids','get').keys()
    while res in __existing_session_ids:
        res = "".join(choices(ascii_letters,digits,k=num))
    return res

### this is the user class for which use is defined

class user: 

    def __init__(self,username:str,ip_address:str,session_id:str=id_generate(32),time_of_login:str=dt.now().isoformat(),ft:bool=True) -> None:
        self.username = username
        self.ip_address = ip_address
        self.session_id = session_id
        self.time_of_login = time_of_login
        self.ft = False

        if self.ft is True:
            if log_user(user):
                sm_operator('logged_user','add',self,username)
                sm_operator('session_ids','add',self.session_id)
            else:
                del self

### This function tell the user session is still valid or expired depending upon
### it return True or False as the return to function. It just check the user 
### into the logged_users and check the session_id in set sessions_ids.

@object_validator
def validate(self) -> bool:
    try:
        if (dt.now() - dt.fromisoformat(self.time_of_login)).seconds > re_login_time*60*60:
            self.logout()
            return False
        else:
            if sm_operator('logged_user','authentication',self,self.username):
                return True
            else:
                return False
    except Exception as error:
        log_error(error,validate)
        return False