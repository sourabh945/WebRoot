import asyncio
import websockets
import json
from flask import abort

###############################################

from modules._logger import log_error

###############################################

async def _requester(holder:str,operation:str,object=[],key:str=None):
    async with websockets.connect('ws://0.0.0.0:8001') as server:
        try:
            if holder == "logged_user" and operation != "get":
                object = object.__dict__
            
            elif holder == "parser" and operation != 'get' and operation != 'open_parser':
                _obj , path = object
                object = (_obj.__dict__,path)


            await server.send(json.dumps({'holder':holder,'operation':operation,'object':object,'key':key}))

            _response = await server.recv()
            

            response = json.loads(_response)

            try:
                return response['response']
            except:
                return {}
        except Exception as error:
            log_error(error,_requester)
            return abort(500)
        
async def sm_operator(holder:str,operation:str,object=[],key:str=None):
    return asyncio.run(_requester(holder=holder,operation=operation,object=object,key=key))