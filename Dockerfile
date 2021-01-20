FROM python:3.6.8-slim-stretch

RUN apt-get update --fix-missing

RUN apt-get install -yq ffmpeg vim htop

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "api.py" ]
