# python3.9
from glob import glob
from yt_dlp import YoutubeDL
from os import path
from sqlitedict import SqliteDict
import json
import logging
working_dir = path.abspath(r"./working/")
video_info_db_path = path.abspath(r"./working/video_info.sqlite")
PROCESSED_FILE_EXTENSION = ".mp4.final.mp4"


def get_video_title_by_id(vid):
    with YoutubeDL() as ydl: 
        info_dict = ydl.extract_info(f'https://youtu.be/{vid}', download=False)
        #the first parameter can be id, url, and etc.
        return info_dict.get('title', None)

def create_video_info_db():
    processed_files = glob(f"{working_dir}/*{PROCESSED_FILE_EXTENSION}")
    for file_path in processed_files:
        folder, file_name = path.split(file_path)
        video_id = file_name.replace(PROCESSED_FILE_EXTENSION ,"")
        video_title = None
        try:
            video_title = get_video_title_by_id(video_id)
        except Exception as ex:
            logging.error(f"create_video_info_db:unable to get video title for {video_id}:" + str(ex))
            return

        if video_title:
            try:
                id = video_id.encode('utf-8')
                title = video_title.encode('utf-8')
                get_db()[id] = {"id": id, "title": title}
                logging.info(f"adding {video_id} - {video_title} to the database")
            except Exception as ex:
                logging.error(f"unable to save video info {video_id}:" + str(ex))
def video_info_db_exists():
    return path.isdir(video_info_db_path)

def get_db():
    return SqliteDict(video_info_db_path, autocommit=True)

def add_video_info(id):
    try:
        video_title = get_video_title_by_id(id)
        title = video_title.encode('utf-8')
        get_db()[id] = {"id": id, "title": title}
        return video_title
    except Exception as ex:
        logging.error(f"failed to add video info for {id}:" + str(ex))
        return None
        
def get_video_info_as_map():
    result = {}
    for key, value in get_db().items():
        result[key] = value["title"]
    return result

def ensure_database_exists():
    if not video_info_db_exists():
        logging.error(f"{video_info_db_path} does not exist. It's going to build one.")
        create_video_info_db()



if __name__ == "__main__":
    #res = get_video_title_by_id("SXPnaLGgnPQ")
    #print(res)

    print(get_video_info_as_map())
