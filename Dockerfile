FROM python:3.5
RUN apt-get update && apt-get install -y libpq-dev python-dev \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.1.0/dockerize-linux-amd64-v0.1.0.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.1.0.tar.gz \
    && rm dockerize-linux-amd64-v0.1.0.tar.gz
ADD requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
ADD . /src

WORKDIR /src
EXPOSE 8080

CMD ["python3", "server.py"]