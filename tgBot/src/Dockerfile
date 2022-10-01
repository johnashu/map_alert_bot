FROM python:3.8-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100


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