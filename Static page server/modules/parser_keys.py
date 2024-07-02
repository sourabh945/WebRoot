from random import choices
from string import ascii_letters,digits
from multiprocessing import Manager
from threading import Lock

lock = Lock()

manager = Manager()

######################################################

from modules.error_logger import error_log # the error logging function log error to /log/error_logs.csv
from modules.user import users_module
from modules.path_operators import path_validator , parent_path
from modules.shared_memory import get_parser,add_to_parser,remove_from_parser

######################################################
### This contain the user and its accessing folder information at any instant.
### And this dict are use to pass the user info and the folder info to function
### when we redirect from a webpage / function and to access this function we need 
### a key that have list of user and its accessing folder and the key is random number.


#####################################################
### This function generate a random key every time it called and return 
### And this random string user as the key for the parser dict 

 # it a set of existing keys it use to not have same for two users.

def _key_generator(num:int=16):
    res = "".join(choices(ascii_letters+digits,k=num))
    while res in get_parser().keys():
        res = "".join(choices(ascii_letters+digits,k=num))
    return res

##################################################
### This function take the existing key and new folder and return a new for getting the user and folder
### that can parse to the function/ webpage to access the page
def new_key():
    pass 

###################################################
### this function create the key for first time when user is logged in

def key(user:object,folder_path:str):
    try:
        if users_module.user.validate(user) is True and path_validator(folder_path) is True:
            _key = _key_generator(16)
            add_to_parser(user,folder_path,_key)
            return _key
        return _key_generator(16)
    except Exception as error:
        error_log(error,key)
        return _key_generator(16)
    
########################################################
### this function authenticate parser key
def authenticate_key(parser_key:str) -> bool:
    if parser_key in get_parser().keys():
        return True
    return False
    
#########################################################
### this function return user and the folder_path transfer thought the key in request using parser
### when we use this function parser key used and it used only once

def open_parser(parser_key:str) -> tuple[users_module.user,str]:
    user,filepath = get_parser()[parser_key]
    remove_from_parser(parser_key)
    return (user,filepath)

#######################################################
### this function open the key without remove the key and delete the parser 
### that can be reused to access page but this time the page, but this time 
### file path change to its folder path that contain the file 

# def open_parser_return_again(parser_key:str) -> tuple[users_module.user,str]:
#     user , filepath = parser[parser_key]
#     parser[parser_key] = (user,parent_path(filepath))
#     return (user,filepath)