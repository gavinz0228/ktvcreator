# -*- coding:utf-8 -*-

from os import path, mkdir, system
from os.path import exists

import time
import json
import logging
import asyncio

from spleeter.audio.adapter import AudioAdapter
from spleeter.separator import Separator

ffmpeg_executable = "ffmpeg"
ydl_executable = "yt-dlp"
audio_sampling_rate = 44100

working_dir = path.abspath(r"./working/")
images_dir = path.abspath(r"./images/")
templates_dir = path.abspath(r"./templates/")
separator = Separator('spleeter:2stems')

async def run_shell_get_output(command):
    return await asyncio.subprocess.check_output(command, shell=True, text = True)
   
async def run_shell(command):
    process = await asyncio.create_subprocess_shell(
        '/bin/bash',
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)

    out, err = await process.communicate(bytes(command, 'utf-8'))
    if err:
        raise Exception(err)
    return out.decode("utf-8")

async def get_video_name(url):
    video_name = await run_shell(f'{ydl_executable} -f "bestvideo[ext=mp4]" {url} --get-filename -o "%(id)s.%(ext)s"')
    return video_name.strip()

async def download_yt_video(url, folder_dir):
    media_name = await get_video_name(url)
    file_name = media_name
    logging.info(file_name)
    output_path = path.join(folder_dir,file_name)
    await run_shell(f'{ydl_executable} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" {url} -o "{output_path}"')
    logging.info(output_path)
    return output_path #, path.exists(output_path)


async def remove_video_vocal(video_file_path):
    logging.info("extracting audio")
    audio_with_vocal = f"{video_file_path}.audio.mp4";
    if not exists(audio_with_vocal):
        res = await run_shell(f"{ffmpeg_executable} -i {video_file_path} -c copy -map 0:a {audio_with_vocal}")
        logging.info(res)
    logging.info("removing vocal")
    audio_without_vocal = f"{video_file_path}.audio_no_vocal.mp4";
    if not exists(audio_without_vocal):
        remove_audio_vocal(audio_with_vocal, audio_without_vocal)
    final_output = f"{video_file_path}.final.mp4"
    logging.info("attaching non-vocal sound back to video")
    if not exists(final_output):
        res = await run_shell(f"ffmpeg -i {video_file_path} -i {audio_without_vocal} -map 0:v -map 1:a -c:v copy -shortest {final_output}")
        logging.info(res)
    return final_output

def remove_audio_vocal(audio_file_path, output_path):
    # have to use AudioAdapter.DEFAULT instead of AudioAdapter.default() in docker
    audio_loader = None
    if hasattr(AudioAdapter, 'DEFAULT'):
        audio_loader = AudioAdapter.DEFAULT
    else: 
        audio_loader = AudioAdapter.default()
    logging.info("loading audio with spleeter")
    waveform, _ = audio_loader.load(audio_file_path, sample_rate=audio_sampling_rate)
    # Perform the separation :
    logging.info("performing vocal spliting" + str(waveform))
    prediction = None
    try:
        prediction = separator.separate(waveform)
    except Exception as e:
        logging.error("failed to split vocal")
        logging.error(e)
        return None
    logging.info("saving non-vocal sound")
    audio_loader.save(output_path, prediction['accompaniment'], audio_sampling_rate)

async def remove_vocal_for_youtube_url(yt_url):
    video_path = await download_yt_video(yt_url, working_dir)
    logging.info("removing vocal: " + video_path)
    result = await remove_video_vocal(video_path)
    logging.info("finished removing vocal" + result)
    return result
    
async def remove_vocal_for_local_video(video_path):
    result = await remove_video_vocal(video_path)
    logging.info("finished removing vocal" + result)
    return result
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    working_dir = path.abspath(r"./working/")
    #url = "https://www.youtube.com/watch?v=ga5Lb9JTxx8"
    url = "https://www.youtube.com/watch?v=qlvE_owkBwI"
    print(asyncio.run(remove_vocal_for_youtube_url(url)))
    #remove_audio_vocal("Eagles_Hotel_California.mp3", "./Eagles_Hotel_California.mp3.mmo.mp3")