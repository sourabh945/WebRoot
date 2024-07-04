import asyncio
import websockets
import json
from flask import abort

############################################################

from modules.error_logger import error_log

############################################################

### This code 

async def server_requester(holder:str,operation:str,object=None,key:str=None):
    async with websockets.connect('ws://0.0.0.0:8001') as server:
        try:
            obj = []
            if holder == "logged_user" and operation != 'get':
                obj = object.__dict__
            elif holder == "parser" and operation != 'get':
                user,path = object
                obj = (user.__dict__,path)
            
            await server.send(json.dumps({'holder':holder,'operation':operation,'object':obj,'key':key}))

            _response = await server.recv()

            response = json.loads(_response)

            server.close_connection()

            return response
        except Exception as error:
            error_log(error,server_requester)
            return abort(500)

    
def shared_memory_operator(holder:str,operation:str,object=None,key:str=None):
    return asyncio.run(server_requester(holder,operation,object,key))
