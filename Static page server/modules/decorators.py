from flask import redirect , request , abort
from functools import wraps

######################################################

################# modules imports ####################

from modules.error_logger import error_log , other_error_logger
from modules.parser_keys import authenticate_key , open_parser , open_parser_return_again
from modules.path_operators import path_validator
from modules.user import users_module


####################################################

################ pre-check decorator ##################

### This decorator help to pre operation like user session authentication, path request validator , key authentications 
### and this for a security of the files and make it any one without authorization can't access the files

def pre_authentication(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            parser_key = request.args["parser_key"]
        except Exception as error:
            error_log(error,func)
            return redirect("/login")
        if authenticate_key(parser_key) is False:
            abort(401)
        else:
            user, folder_path = open_parser(parser_key)
            if users_module.user.validate(user) is True:
                if path_validator(folder_path) is True:
                    return func(user,folder_path)
                else:
                    other_error_logger("Invalid folder_path in parser",f"This is due to invalid and non accessible folder path is parser and key is authenticated and user also but not path and user is {user.username}",func)
                    abort(500)
            else:
                return redirect("/login")
    return wrapper 

###########################################################

### this is decorate works same as upper decorator "pre_authenticator" but this 
### it doesn't expire the pervious page so user can access page after the download

def pre_authentication_download(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            parser_key = request.args["parser_key"]
        except Exception as error:
            error_log(error,func)
            return redirect("/login")
        if authenticate_key(parser_key) is False:
            abort(401)
        else:
            user , file_path = open_parser_return_again(parser_key)
            if users_module.user.validate(user) is True:
                if path_validator(file_path) is True:
                    return func(user,file_path)
                else:
                    other_error_logger("Invalid folder_path in parser",f"This is due to invalid and non accessible folder path is parser and key is authenticated and user also but not path and user is {user.username}",func)
                    abort(500)
            else:
                return redirect("/login")
    return wrapper 