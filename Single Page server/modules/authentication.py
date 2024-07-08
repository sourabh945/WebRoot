import os 
import json

################# modules imports ##################################

from modules._logger import log_error

################# path imports #####################################

from _paths import users_cred_file

##################### functions ######################################

### authenticate user credential ####################################

def load_cred():
    try:
        with open(users_cred_file,'r') as file:
            users_credentials = json.load(file)
        return users_credentials
    except Exception as error:
        log_error(error,load_cred)
        raise Exception

users_credentials = load_cred()

def authenticate_user_cred(username:str,password:str) -> bool:
    if username in users_credentials.keys() and users_credentials['username'] == password:
        return True
    else:
        return False


### 