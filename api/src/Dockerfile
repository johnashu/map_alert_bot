FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# set environment variables..j.
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# # set work directory
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3.9
    
# RUN pip3 install pipenv gunicorn uvicorn[standard] requests curlify

# copy project
COPY . /usr/src 

RUN pip3 install -r /usr/src/requirements.txt