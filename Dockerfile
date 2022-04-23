FROM python:3.10.0-alpine

WORKDIR /nucleos

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /nucleos/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .