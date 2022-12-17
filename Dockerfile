FROM ubuntu:20.04

WORKDIR /usr/src/app
RUN mkdir working

COPY requirements.txt ./
RUN apt update
RUN apt -y install python3.9
RUN apt -y install pip
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt -y install ffmpeg
RUN apt -y install nvidia-cuda-toolkit

COPY *.py ./

#CMD [ "python3", "./server.py" ]
CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:80","server:app"]
EXPOSE 80