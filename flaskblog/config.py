from pathlib import Path
import os


class Config:
    # config
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    # check if we're in a docker
    if os.getcwd() == "/code":
        full_path = Path(Path(Path.cwd()).parent / "config")
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(full_path, "site.db")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            os.getcwd(), "workingdb.db"
        )

    # mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
