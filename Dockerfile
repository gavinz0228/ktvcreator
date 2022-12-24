FROM gavin0228/ktvcreator_base:1.0

WORKDIR /usr/src/app

COPY *.py ./
RUN mkdir templates
COPY ./templates/*.html ./templates

ENV NUMBER_OF_WORKERS=1
ENV WORKER_TIMEOUT=120

#CMD [ "python3", "./server.py" ]
CMD ["sh", "-c", "python3 -m gunicorn -w ${NUMBER_OF_WORKERS} -t ${WORKER_TIMEOUT} -b 0.0.0.0:80 server:app"]
EXPOSE 80
