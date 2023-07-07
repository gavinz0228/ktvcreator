from aiohttp import web
from os import path
from processor import remove_video_vocal, download_yt_video, remove_vocal_for_youtube_url, working_dir, images_dir, templates_dir
from processing_server import start_processing_server
from video_info import * 
from threading import Thread
from pathlib import Path


import asyncio
import logging
import websockets
import socket

WEB_SOCKET_PING_TIMEOUT = 10 * 60
WEB_SOCKET_PROCESSING_SERVER_HOST = "127.0.0.1"
WEB_SOCKET_PROCESSING_SERVER_PORT = 60000
MAX_RECENT_FILES = 50

ensure_database_exists()

def is_websocket_server_running(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return  sock.connect_ex((host, port)) == 0
    except Exception as e:
        return False

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
    video_id = Path(final_output).name.split(".")[0]
    video_title = add_mapping_for_video_id(video_id)
    if video_title:
        logging.info(f'{video_id}:{video_title}')
    else:
        logging.error(f'Failed to get video title for video_id:{video_id}')
    return web.Response(text=video_id) 

async def recent_files(request):
    files = list(filter(path.isfile, glob(f'{working_dir}/*{PROCESSED_FILE_EXTENSION}')))
    files.sort(key=lambda x: path.getmtime(x), reverse=True)
    
    video_info_map = get_video_info_as_map()

    i = 0
    res = []

    for file_path in files:
        folder, file_name = path.split(file_path)
        video_id = file_name.replace(PROCESSED_FILE_EXTENSION ,"")
        # some videos are deleted on youtube, and it might not be in the name map
        if video_id.encode('utf-8') in video_info_map:
            res.append({"videoId":video_id, "videoName":video_info_map[video_id.encode('utf-8')].decode('utf-8')})
            i += 1
            if i == MAX_RECENT_FILES:
                break

    return web.json_response(res)

if not is_websocket_server_running(WEB_SOCKET_PROCESSING_SERVER_HOST, WEB_SOCKET_PROCESSING_SERVER_PORT):
    logging.info("websocket processing server is not yet started, starting it right now.")
    worker = Thread(target=start_processing_server, args=(WEB_SOCKET_PROCESSING_SERVER_HOST, WEB_SOCKET_PROCESSING_SERVER_PORT))
    worker.start()
else:
    logging.info("websocket processing server is already running.")


app = web.Application()
app.add_routes([web.get('/', home),
                web.get('/process', process),
                web.get('/recent_files', recent_files),
                web.static('/images/', images_dir),
                web.static('/download/', working_dir)
])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=80)
    #print(is_websocket_server_running("localhost", 60000))