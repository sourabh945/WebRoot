import json

###############################################

from modules.error_logger import error_log # this is for log every error
from _paths import _user_login_credential_path

###############################################
### Ths function read the user_credential file store in database folder and load the 
### json into the program and use to validate the user

def load_credentials() -> list:
    try:
        with open(_user_login_credential_path,"r") as file:
            credentials = json.load(file)
        return credentials
    except Exception as error:
        error_log(error,load_credentials)
        return []
    
#################################################

login_credentials = load_credentials() # this dict is for store the login credentials 
# i suggest that, it is useful only when you have very low user counts (like less 10000)

#################################################

### this function authenticate the user credentials that stored in file

def authenticate_user(username:str,password:str) -> bool:
    try:
        if username in login_credentials.keys() and login_credentials[username] == password:
            return True
        else:
            return False
    except Exception as error:
        error_log(error,authenticate_user)
        return False
    
