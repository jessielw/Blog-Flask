# Blog (Created in Flask)

This is a simple project that's complete with forums and functional to be utilized standalone/docker

Developed by Jessie Wilson (2023)

## Required enviormental variables

`EMAIL_USER` Gmail account setup to send forgot password emails to registered users

`EMAIL_PASSWORD` Gmail account with an "app password"

`FLASK_SECRET_KEY` A secret string of your choosing e.g. "asfasdoiuqwe31234"

## Basic Usage

You can just execute run_app.py to start the webserver in a windows/linux/mac enviorment 

## Docker Usage 

`https://hub.docker.com/repository/docker/jlw4049/flask_blog/`

You must pass all of the "Required enviormental variables" to your docker.

Additionally if you are hosting this in a subfolder and using a webserver such as gunicorn you must pass an additional variable script_name

`SCRIPT_NAME` pass the base name e.g. "/flask"

You should map port `8000`

Set a path path variable `/config` to where ever you want the images/db to be stored outside of the docker container