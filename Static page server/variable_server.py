import asyncio
import websockets
import json


global data 

data = {'parser':{},'logged_user':{},'session_ids':[]}

auth_key = 'XNz9hQ6uM4IOnIQFf1Bn8CDXfEKIoWGY'

async def handler(websocket):
    _request = await websocket.recv()
    
    request = json.loads(_request)

    response = json.dumps({})

    if request['operation'] == 'get':
        response = json.dumps(data[request['holder']])

    elif request['operation'] == 'add':
        if request['holder'] == 'session_ids':
            data[request['holder']].append(request['object'])
        else:
            data[request['holder']][request['key']] = request['object']
    
    elif request['operation'] == 'remove':
        if request['holder'] == 'session_ids':
            data[request['holder']].remove(request['object'])
        else:
            del data[request['holder']][request['key']]

    await websocket.send(response)

async def main():
    async with websockets.serve(handler,"localhost",8001) :
        await asyncio.Future()

if __name__ == "__main__":
    print("Server is start ...")
    asyncio.run(main())