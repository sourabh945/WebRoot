from random import choices
from string import ascii_letters,digits

from flask import abort

######################################################

from modules.error_logger import error_log # the error logging function log error to /log/error_logs.csv
from modules.user import users_module # the modules for user class
from modules.path_operators import path_validator # to validate the path
from modules.shared_memory_client import gar_operator # to variable from the shared memory that run on different server

#####################################################
### This function generate a random key every time it called and return 
### And this random string user as the key for the parser dict 

 # it a set of existing keys it use to not have same for two users.

def _key_generator(num:int=16):
    res = "".join(choices(ascii_letters+digits,k=num))
    _existing_keys = gar_operator('parser','get').keys()
    while res in _existing_keys:
        res = "".join(choices(ascii_letters+digits,k=num))
    return res

###################################################
### this function create the key for first time when user is logged in

def key(user:object,folder_path:str):
    try:
        if path_validator(folder_path) is True:
            _key = _key_generator(16)
            gar_operator('parser','add',(user,folder_path),_key)
            return _key
        return abort(401)
    except Exception as error:
        error_log(error,key)
        return abort(500)
    
#########################################################
### this function is for authenticate the parser keys we get

def authenticate_key(parser_key:str):
    return  gar_operator('key','authentication',parser_key) 
       
    
#########################################################
### this function return user and the folder_path transfer thought the key in request using parser
### when we use this function parser key used and it used only once

def open_parser(parser_key:str) -> tuple[users_module.user,str]:
    _user,filepath = gar_operator('parser','open_parser',key=parser_key)
    user = users_module.user(**_user)
    if path_validator(filepath) is True:
        return (user , filepath)
    abort(500)

############################################################################################3