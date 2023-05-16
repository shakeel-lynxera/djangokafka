##
FROM python:3.7

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt update
RUN apt install -y cron

COPY . .
RUN cp env-prod .env
RUN cat .env
