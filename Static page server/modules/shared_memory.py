from modules.shared_memory_client import shared_memory_operator

from modules.user import users_module

def get_object(holder:str):
    data = shared_memory_operator(holder,'get')
    if holder == 'logged_user':
        result = {}
        for i in data.keys():
            result[i] = users_module.user(**data[i])
        return result
    elif holder == 'parser':
        result = {}
        for i in 
    return shared_memory_operator(holder,'get')

def add_to_object(holder:str,adder:any,_key:str=""):
    global data
    if holder == "session_ids":
        data['manager_dict'][holder].add(adder)
    else:
        data['manager_dict'][holder][_key] = adder
    
def remove_from_object(holder:str,remover:any=None,_key:str=""):
    global data
    if holder == "session_ids":
        data['manager_dict'][holder].remove(remover)
    else:
        del data['manager_dict'][holder][_key]
    

#################################################

### function for parser ########################

def get_parser() -> dict:
    return get_object('parser')
    
def add_to_parser(user:object,folder_path:str,key:str) -> None:
    return add_to_object('parser',(user,folder_path),key)

def remove_from_parser(key:str) -> None:
    return remove_from_object('parser',None,key)

#### function for logged_user #######################

def get_logged_user() -> dict:
    return get_object('logged_user')

def add_to_logged_user(username:str,user:object) -> None:
    return add_to_object('logged_user',user,username)

def remove_from_logged_user(username:str) -> None:
    return remove_from_object('parser',None,username)

#### function for session_ids ###########################

def get_session_ids() -> set:
    return get_object('session_ids')

def add_to_session_ids(session_id:str) -> None:
    return add_to_object('session_ids',session_id)

def remove_from_session_ids(session_id:str) -> None:
    return remove_from_object('session_ids',session_id)