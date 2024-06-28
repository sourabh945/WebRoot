from random import choices
from string import ascii_letters,digits

######################################################

from modules.error_logger import error_log # the error logging function log error to /log/error_logs.csv
from modules.user import users_module
from modules.path_operators import path_validator

######################################################
### This contain the user and its accessing folder information at any instant.
### And this dict are use to pass the user info and the folder info to function
### when we redirect from a webpage / function and to access this function we need 
### a key that have list of user and its accessing folder and the key is random number.

parser = dict()

#####################################################
### This function generate a random key every time it called and return 
### And this random string user as the key for the parser dict 

_existing_keys = set() # it a set of existing keys it use to not have same for two users.

def _key_generator(num:int=16):
    res = "".join(choices(ascii_letters+digits,num))
    while res in _existing_keys:
        res = "".join(choices(ascii_letters+digits,num))
    return res

##################################################
### This function take the existing key and new folder and return a new for getting the user and folder
### that can parse to the function/ webpage to access the page

def new_key(existing_key:str,folder_path:str=None) -> str:
    try:
        if _existing_keys not in parser.keys():
            return ""
        user, old_folder_path = parser[existing_key]
        _existing_keys.remove(existing_key)
        del parser[existing_key]
        _new_key = _key_generator(10)
        if folder_path is None:
            folder_path = old_folder_path
        parser[_new_key] = (user,folder_path)
        return _new_key
    except Exception as error:
        error_log(error,new_key)
        return _key_generator(16)
    
###################################################
### this function create the key for first time when user is logged in

def key(user:object,folder_path:str):
    try:
        if users_module.user.validate(user) is True and path_validator(folder_path) is True:
            _key = _key_generator(16)
            parser[_key] = [user,folder_path]
            return _key
        return _key_generator(16)
    except Exception as error:
        error_log(error,key)
        return _key_generator(16)
    
########################################################
### this function authenticate parser key
def authenticate_key(parser_key:str) -> bool:
    return True if parser_key in _existing_keys else False
    
#########################################################
### this function return user and the folder_path transfer thought the key in request using parser
### when we use this function parser key used and it used only once

def open_parser(parser_key:str) -> tuple[object,str]:
    user,filepath = parser[parser_key]
    del parser[parser_key]
    _existing_keys.remove(parser_key)
    return tuple(user,filepath)
