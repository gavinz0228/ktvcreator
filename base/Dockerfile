FROM ubuntu:20.04

WORKDIR /usr/src/app
RUN mkdir working
COPY *.py ./

RUN apt update
RUN apt -y install ffmpeg
RUN apt -y install nvidia-cuda-toolkit

RUN apt -y install python3.9
RUN apt -y install pip

RUN pip install spleeter
#RUN apt install -y software-properties-common
#RUN add-apt-repository ppa:deadsnakes/ppa
#RUN apt update

#RUN apt -y install python3.10
#RUN apt -y install python3.10-distutils
#RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
#RUN python3.10 ./get_pip.py
#RUN apt -y install python3-pip
#RUN python3.10 -m pip install --upgrade pip

#COPY requirements.txt ./
#RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

#CMD [ "python3", "./server.py" ]
#CMD ["sh", "-c", "python3.10 -m gunicorn -w ${NUMBER_OF_WORKERS} -t ${WORKER_TIMEOUT} -b 0.0.0.0:80 server:app"]
#EXPOSE 80
