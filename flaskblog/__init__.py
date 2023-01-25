from pathlib import Path
import shutil
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

# mail settings
mail = Mail()

# set static directory
if Path(Path(Path.cwd()).parent / "config").exists():
    app_data = Path(Path(Path.cwd()).parent / "config")
    shutil.copytree(
        Path(Path.cwd()) / "flaskblog" / "static", app_data, dirs_exist_ok=True
    )
else:
    app_data = "static"


def create_app(config_class: object = Config):
    app = Flask(__name__, static_folder=app_data)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import routes
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    # create table from models if it doesn't exist
    from flaskblog.models import create_table_if_not_exist

    create_table_if_not_exist(app)

    for bp in [users, posts, main, errors]:
        app.register_blueprint(bp)

    return app
