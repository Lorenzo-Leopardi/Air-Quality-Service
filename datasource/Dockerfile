# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/datasource
COPY requirements.txt /code/datasource
RUN pip install -r requirements.txt
COPY . /code/datasource