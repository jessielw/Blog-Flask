# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w" , "2", "-b", "0.0.0.0:8000", "flaskblog:create_app()", "--reload"]