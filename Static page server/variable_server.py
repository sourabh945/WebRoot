import asyncio
import websockets
import json


global data 

data = {'parser':{},'logged_user':{},'session_ids':[]}

auth_key = 'XNz9hQ6uM4IOnIQFf1Bn8CDXfEKIoWGY'

async def handler(websocket):
    _request = await websocket.recv()
    
    request = json.loads(_request)

    response = {}

    if request['operation'] == 'get':
        response = {'response':data[request['holder']]}

    elif request['operation'] == 'add':

        if request['holder'] == 'session_ids':

            data[request['holder']].append(request['object'])

        elif request['holder'] == 'logged_user':

            if request['key'] in data['logged_user'].keys():
                response = {'response':True}
                data['session_ids'].remove(request['object']['session_id'])

            else:
                response = {'response':False}
            data[request['holder']][request['key']] = request['object']

        else:
            data[request['holder']][request['key']] = request['object']
    
    elif request['operation'] == 'remove':

        if request['holder'] == 'session_ids':
            data[request['holder']].remove(request['object'])

        else:
            del data[request['holder']][request['key']]

    elif request['operation'] == 'open_parser' and request['holder'] == "parser":
        response = {'response':data['parser'][request['key']]}
        del data['parser'][request['key']]

    elif request['operation'] == 'authentication' :

        if request['holder'] == 'key':

            if request['object'] in dict(data['parser']).keys():
                response = {'response':True}

            else:
                response = {'response':False}

        elif request['holder'] == 'logged_user':

            if request['object'] == (data['logged_user'])[str(request['key'])] and request['object']['session_id'] in set(data['session_ids']):
                response = {'response':True}

            else:
                response = {'response':False}

    response = json.dumps(response)

    await websocket.send(response)

async def main():
    async with websockets.serve(handler,"localhost",8001,) :
        await asyncio.Future()

if __name__ == "__main__":
    print("Server is start ...")
    asyncio.run(main())