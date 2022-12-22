FROM ubuntu:20.04

WORKDIR /usr/src/app
RUN mkdir working

RUN apt update
RUN apt -y install python3.9
RUN apt -y install pip
RUN apt -y install ffmpeg
RUN apt -y install nvidia-cuda-toolkit

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

#CMD [ "python3", "./server.py" ]
CMD ["sh", "-c", "python3 -m gunicorn -w ${NUMBER_OF_WORKERS} -t ${WORKER_TIMEOUT} -b 0.0.0.0:80 server:app"]
EXPOSE 80
