# python3.9
from glob import glob
from yt_dlp import YoutubeDL
from os import path
import json
import logging
working_dir = path.abspath(r"./working/")
name_map_path = path.abspath(r"./name_map.json")
PROCESSED_FILE_EXTENSION = ".mp4.final.mp4"

def get_video_title_by_id(vid):
    with YoutubeDL() as ydl: 
        info_dict = ydl.extract_info(f'https://youtu.be/{vid}', download=False)
        #the first parameter can be id, url, and etc.
        return info_dict.get('title', None)

def build_name_map():
    processed_files = glob(f"{working_dir}/*{PROCESSED_FILE_EXTENSION}")
    name_map = {}
    for file_path in processed_files:
        folder, file_name = path.split(file_path)
        video_id = file_name.replace(PROCESSED_FILE_EXTENSION ,"")
        try:
            video_title = get_video_title_by_id(video_id)
            name_map[video_id] = str(video_title)
        except Exception as ex:
            logging.error(f"build_name_map:unable to get video title for {video_id}:" + str(ex))

    save_name_map(name_map)

def name_map_exists():
    return path.isfile(name_map_path)

def add_mapping_for_video_id(video_id):
    name_map = get_name_map()
    try:
        video_title = get_video_title_by_id(video_id)
        name_map[video_id] = str(video_title)
        save_name_map(name_map)
        return video_title
    except Exception as ex:
        logging.error(f"add_mapping_for_video_id:unable to get video title for {video_id}:" + str(ex))
        return None
        
def ensure_name_map_exists():
    if not name_map_exists():
        logging.error(f"{name_map_path} does not exist. It's going to build one.")
        build_name_map()

def get_name_map():
    with open(name_map_path, 'r') as openfile:
        return json.load(openfile)

def save_name_map(name_map):
    with open(name_map_path, "w") as outfile:
        json.dump(name_map, outfile)


if __name__ == "__main__":
    #res = get_video_title_by_id("SXPnaLGgnPQ")
    #print(res)
    #ensure_name_map_exists()
    #build_name_map()
    print(get_name_map())