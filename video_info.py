# python3.9
from glob import glob
from yt_dlp import YoutubeDL
from os import path
import json
import logging
import rocksdb
working_dir = path.abspath(r"./working/")
video_info_db_path = path.abspath(r"./working/video_info.db")
PROCESSED_FILE_EXTENSION = ".mp4.final.mp4"

def get_video_title_by_id(vid):
    with YoutubeDL() as ydl: 
        info_dict = ydl.extract_info(f'https://youtu.be/{vid}', download=False)
        #the first parameter can be id, url, and etc.
        return info_dict.get('title', None)

def create_video_info_db():
    processed_files = glob(f"{working_dir}/*{PROCESSED_FILE_EXTENSION}")
    db = get_db()
    for file_path in processed_files:
        folder, file_name = path.split(file_path)
        video_id = file_name.replace(PROCESSED_FILE_EXTENSION ,"")
        try:
            video_title = get_video_title_by_id(video_id)
            db.put(video_id.encode('utf-8'), video_title.encode('utf-8'))
            logging.info(f"adding {video_id} - {video_title} to the database")
        except Exception as ex:
            logging.error(f"create_video_info_db:unable to get video title for {video_id}:" + str(ex))

def video_info_db_exists():
    return path.isdir(video_info_db_path)

def get_db():
    return rocksdb.DB(video_info_db_path, rocksdb.Options(create_if_missing=True))

def add_video_info(id):
    try:
        video_title = get_video_title_by_id(id)
        get_db().put(id.encode('utf-8'), video_title.encode('utf-8'))
        return video_title
    except Exception as ex:
        logging.error(f"create_video_info_db:unable to get video title for {video_id}:" + str(ex))
        return None
        
def get_video_info_as_map():
    it = get_db().iteritems()
    it.seek_to_first()
    return dict(it)
    

def ensure_database_exists():
    if not video_info_db_exists():
        logging.error(f"{video_info_db_path} does not exist. It's going to build one.")
        create_video_info_db()



if __name__ == "__main__":
    #res = get_video_title_by_id("SXPnaLGgnPQ")
    #print(res)

    print(get_video_info_as_map())