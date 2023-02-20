# ktvcreator
A simple web server written in python to remove vocal for youtube videos. I runs a separated websocket service that's only responsible for video/audio processing, to ensure there will only one video being processed at any given time to limit memory usage.  
  
Web Framework: aiohttp  
video/Audio Processing: ffmpeg  
vocal Removing library: Spleeter  
  
  
To build the base image(with a version number):
sudo docker build ./base -t gavin0228/ktvcreator_base:1.0

To build the final image(with a version number):
sudo docker build . -t gavin0228/ktvcreator:1.0