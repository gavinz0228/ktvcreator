import asyncio
import websockets
import socket
import logging
from processor import remove_vocal_for_youtube_url


async def handler(websocket, path):
    data = await websocket.recv()
    logging.info("received: ", data)
    reply = await remove_vocal_for_youtube_url(data)
    await websocket.send(reply)
 
def start_processing_server(host, port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    start_server = websockets.serve(handler, host, port)
    logging.info("starting up websocket processing server: ", host, ":", port)
    
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    start_processing_server("localhost", 60000)