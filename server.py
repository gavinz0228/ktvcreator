from aiohttp import web
from os import path
from processor import remove_video_vocal, download_yt_video, remove_vocal_for_youtube_url, working_dir, images_dir, templates_dir
from processing_server import start_processing_server
from threading import Thread
from pathlib import Path
import asyncio
import logging
import websockets
import socket
WEB_SOCKET_PING_TIMEOUT = 10 * 60
WEB_SOCKET_PROCESSING_SERVER_HOST = "127.0.0.1"
WEB_SOCKET_PROCESSING_SERVER_PORT = 60000

def is_websocket_server_running(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return  sock.connect_ex((host, port)) == 0

def html_response(document):
    s = open(path.join(templates_dir, document), "r")
    return web.Response(text=s.read(), content_type='text/html')

async def home(request):
    return html_response("index.html")

async def process(request):
    if "url" not in request.rel_url.query:
        return web.Response(text="url param is not presented in the url!")
    yt_url = request.rel_url.query["url"].strip()
    if not yt_url:
        return web.Response(text="youtube url is not presented, please paste your youtube url after ?url=") 

    #final_output = await remove_vocal_for_youtube_url(yt_url)
    async with websockets.connect(f'ws://{WEB_SOCKET_PROCESSING_SERVER_HOST}:{WEB_SOCKET_PROCESSING_SERVER_PORT}', ping_timeout=WEB_SOCKET_PING_TIMEOUT) as websocket:
        await websocket.send(yt_url)
        final_output = await websocket.recv()
    logging.info(final_output)

    return web.Response(text=Path(final_output).name.split(".")[0]) 
    

if not is_websocket_server_running(WEB_SOCKET_PROCESSING_SERVER_HOST, WEB_SOCKET_PROCESSING_SERVER_PORT):
    logging.info("websocket processing server is not yet started, starting it right now.")
    worker = Thread(target=start_processing_server, args=(WEB_SOCKET_PROCESSING_SERVER_HOST, WEB_SOCKET_PROCESSING_SERVER_PORT))
    worker.start()
else:
    logging.info("websocket processing server is already running.")

app = web.Application()
app.add_routes([web.get('/', home),
                web.get('/process', process),
                web.static('/images/', images_dir),
                web.static('/download/', working_dir)
])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=80)
    #print(is_websocket_server_running("localhost", 60000))