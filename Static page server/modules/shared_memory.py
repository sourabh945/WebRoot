from multiprocessing import Manager , Process , Queue , Lock 
import multiprocessing

manager = Manager()

lock = Lock()

shared_dict = manager.dict({'parser':{},'logged_user':{},'session_ids':set()})

def get_object(holder:str):
    def func(shared_dict,result,holder):
        result.put(shared_dict[holder])
    result = Queue()
    
    process = Process(target=func,args=(shared_dict,result,holder))
    process.start()
    process.join()
    return result.get()

def add_to_object(holder:str,adder:any,_key:str=""):
    def func(shared_dict,holder,adder,_key):
        if holder == "session_ids":
            shared_dict[holder].add(adder)
        else:
            shared_dict[holder][_key] = adder
    with lock:
        process = Process(target=func,args=(shared_dict,holder,adder,_key))
        process.start()
    process.join()
    
def remove_from_object(holder:str,remover:any=None,_key:str=""):
    def func(shared_dict,holder,remover,_key):
        if holder == "session_ids":
            shared_dict[holder].remove(remover)
        else:
            del shared_dict[holder][_key]
    with lock:
        process = Process(target=func,args=(shared_dict,holder,remover,_key))
        process.start()
        process.join()
    

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