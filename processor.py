# -*- coding:utf-8 -*-

import time
import json
from os import path, mkdir, system
from os.path import exists
import subprocess

from spleeter.audio.adapter import AudioAdapter
from spleeter.separator import Separator

ffmpeg_executable = "ffmpeg"
ydl_executable = "yt-dlp"
audio_sampling_rate = 44100

def run_shell_get_output(command):
    return subprocess.check_output(command, shell=True, text = True)
   
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
    run_shell(f'{ydl_executable} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" {url} -o "{output_path}"')
    print(output_path)
    return output_path #, path.exists(output_path)


def remove_video_vocal(video_file_path):
    print("extracting audio")
    audio_with_vocal = f"{video_file_path}.audio.mp4";
    if not exists(audio_with_vocal):
        run_shell(f"{ffmpeg_executable} -i {video_file_path} -c copy -map 0:a {audio_with_vocal}")
    print("removing vocal")
    audio_without_vocal = f"{video_file_path}.audio_no_vocal.mp4";
    if not exists(audio_without_vocal):
        remove_audio_vocal(audio_with_vocal, audio_without_vocal)
    final_output = f"{video_file_path}.final.mp4"
    if not exists(final_output):
        run_shell(f"ffmpeg -i {video_file_path} -i {audio_without_vocal} -map 0:v -map 1:a -c:v copy -shortest {final_output}")
    return final_output
    
def remove_audio_vocal(audio_file_path, output_path):
    separator = Separator('spleeter:2stems')
    # have to use AudioAdapter.DEFAULT instead of AudioAdapter.default() in docker
    audio_loader = AudioAdapter.DEFAULT
    waveform, _ = audio_loader.load(audio_file_path, sample_rate=audio_sampling_rate)

    # Perform the separation :
    prediction = separator.separate(waveform)
    audio_loader.save(output_path, prediction['accompaniment'], audio_sampling_rate)


if __name__ == "__main__":
    working_dir = path.abspath(r"./working/")
    #url = "https://www.youtube.com/watch?v=ga5Lb9JTxx8"
    url = "https://www.youtube.com/watch?v=qlvE_owkBwI"
    video_path = download_yt_video(url, working_dir)
    print(video_path)
    res = remove_video_vocal(video_path)
    print(res)
    #remove_audio_vocal("Eagles_Hotel_California.mp3", "./Eagles_Hotel_California.mp3.mmo.mp3")