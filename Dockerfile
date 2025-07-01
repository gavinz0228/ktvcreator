FROM gavin0228/ktvcreator_base:1.0

WORKDIR /usr/src/app

COPY get_pip.py ./


RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update

RUN apt -y install python3.10
RUN apt -y install python3.10-distutils
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN python3.10 ./get_pip.py

RUN python3.10 -m pip install --upgrade pip
RUN python3.10 -m pip install --upgrade setuptools
RUN python3.10 -m pip install Pyrebase4
RUN python3.10 -m pip install Cython
RUN python3.10 -m pip uninstall numpy

COPY requirements.txt ./
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

COPY *.py ./
RUN mkdir templates
COPY ./templates/*.html ./templates
RUN mkdir images
COPY ./images/*.* ./images

ENV NUMBER_OF_WORKERS=4
ENV WORKER_TIMEOUT=240



#CMD [ "python3", "./server.py" ]
CMD ["sh", "-c", "python3.10 -m gunicorn -w ${NUMBER_OF_WORKERS} -t ${WORKER_TIMEOUT} -b 0.0.0.0:80 --worker-class aiohttp.worker.GunicornWebWorker server:app "]
EXPOSE 80
