import os
import secrets
from pathlib import Path

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from flaskblog import mail


def delete_old_pic(old_pic):
    if "default.jpg" not in old_pic:
        try:
            delete = os.path.join(str(current_app.static_folder), old_pic)
            os.remove(delete)
        except FileNotFoundError:
            pass


def save_picture(form_picture):
    pic_path = os.path.join(str(current_app.static_folder), "images")

    if not os.path.exists(pic_path):
        os.mkdir(pic_path)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(pic_path, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return "images/" + str(picture_fn)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="noreply.jessielw@gmail.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for("users.reset_token", token=token, _external=True)} 

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
