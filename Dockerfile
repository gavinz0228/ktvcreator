FROM gavin0228/ktvcreator_base:1.0

WORKDIR /usr/src/app

COPY *.py ./
RUN mkdir templates
COPY ./templates/*.html ./templates
RUN mkdir images
COPY ./images/*.* ./images

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

ENV NUMBER_OF_WORKERS=4
ENV WORKER_TIMEOUT=120

#CMD [ "python3", "./server.py" ]
CMD ["sh", "-c", "python3 -m gunicorn -w ${NUMBER_OF_WORKERS} -t ${WORKER_TIMEOUT} -b 0.0.0.0:80 --worker-class aiohttp.worker.GunicornWebWorker server:app "]
EXPOSE 80
