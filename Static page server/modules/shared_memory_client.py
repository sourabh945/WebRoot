import asyncio
import websockets
import json
from flask import abort

############################################################################

from modules.error_logger import error_log

############################################################################

### This function connect to var_server it can able to get , add ,remove the variable 
### the dicts or set we use in the app

async def server_requester(holder:str,operation:str,object=[],key:str=None):
    async with websockets.connect('ws://0.0.0.0:8001') as server:
        try:
            if holder == "logged_user" and operation != "get":
                object = object.__dict__
            
            elif holder == "parser" and operation != 'get' and operation != 'open_parser':
                _obj , path = object
                object = (_obj.__dict__,path)

            print({'holder':holder,'operation':operation,'object':object,'key':key})

            await server.send(json.dumps({'holder':holder,'operation':operation,'object':object,'key':key}))

            _response = await server.recv()
            

            response = json.loads(_response)

            print(response)

            try:
                return response['response']
            except:
                return {}
        except Exception as error:
            error_log(error,server_requester)
            return abort(500)

### this function is the caller function for upper function 
    
def gar_operator(holder:str,operation:str,object=[],key:str=None):
    return asyncio.run(server_requester(holder=holder,operation=operation,object=object,key=key))


############################################################################

