
import time
import json
from os import path, mkdir, system
from os.path import exists
import subprocess
import youtube_dl

from spleeter.audio.adapter import AudioAdapter
from spleeter.separator import Separator

#youtube_dl_executable = path.abspath(r"youtube-dl.exe")
ffmpeg_executable = "ffmpeg"
ydl_executable = "yt-dlp"

def run_shell(command):
    process = subprocess.Popen(
        '/bin/bash',
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    out, err = process.communicate(bytes(command, 'utf-8'))
    if err:
        raise Exception(err)
    return out.decode("utf-8")

def get_video_name(url):
    return run_shell(f'{ydl_executable} -f "bestvideo[ext=mp4]" {url} --get-filename -o "%(id)s.%(ext)s"').strip()

def download_yt_video(url, folder_dir):
    media_name = get_video_name(url)
    file_name = media_name
    print(file_name)
    output_path = path.join(folder_dir,file_name)
    run_shell(f'{ydl_executable} -f "bestvideo[ext=mp4]" {url} -o "{output_path}"')
    print(output_path)
    return output_path #, path.exists(output_path)
    
if __name__ == "__main__":
    working_dir = path.abspath(r"./working/")
    url = "https://www.youtube.com/watch?v=qlvE_owkBwI"
    video_path = download_yt_video(url, working_dir)
    print(video_path)