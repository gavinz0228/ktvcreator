import asyncio
import websockets
import socket
import logging
from processor import remove_vocal_for_youtube_url


async def handler(websocket):
    data = await websocket.recv()
    logging.info("received: ", data)
    reply = await remove_vocal_for_youtube_url(data)
    await websocket.send(reply)
 

async def await_processing_server(host, port):
    logging.info("starting up websocket processing server: ", host, ":", port)
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # Run forever
    
def start_processing_server(host, port):
    asyncio.run(await_processing_server(host, port))


if __name__ == "__main__":
    asyncio.run(start_processing_server("localhost", 60000))