# Flask functions import:
import os

from flask import Flask, render_template
from flask_login import LoginManager

# Blueprints import:
from blueprints.auth import auth_blueprint
from blueprints.general import general_blueprint
from blueprints.mail import mail_blueprint
from blueprints.products import products_blueprint
# Database functions import:
from data import db_session
from data.db_session import create_session
from data.types import Type
from data.users import User

# App initialization:
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('instance.config')
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)

# Use this to run with ngrok (also need to change to app.run() in main())
# from flask_ngrok import run_with_ngrok
# run_with_ngrok(app)

# Blueprints registration:
app.register_blueprint(auth_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(mail_blueprint)
app.register_blueprint(products_blueprint)

# Database setup:
db_session.global_init("db/storage.db")


def get_types():
    """
    Get item types from database.

    :return: List of item types
    """
    db_sess = create_session()  # Create database session
    types = db_sess.query(Type).all()  # Get item types from database
    db_sess.close()  # Shut down database session
    return types


@login_manager.unauthorized_handler
def unauth_handler():
    """
    Unauthorized error handler.

    :return: HTML page with appropriate code
    """
    types = get_types()
    return render_template('error_handler.html', types=types, code="401",
                           name="Unauthorized",
                           description="User is not authorized to access a "
                                       "resource.",
                           message="Чтобы получить доступ к этой странице "
                                   "необходима авторизация.")


@app.errorhandler(404)
def not_found(error):
    """
    Unknown page error handler.

    :param error: "Not found" error
    :type error: werkzeug.exceptions.NotFound
    :return: HTML page with appropriate code
    """
    types = get_types()
    return render_template('error_handler.html', types=types, code=error.code,
                           name=error.name, description=error.description,
                           message="Страница не найдена.")


@app.errorhandler(500)
def internal_error(error):
    """
    Internal server error handler.

    :param error: "Internal server error" error
    :type error: werkzeug.exceptions.InternalServerError
    :return: HTML page with appropriate code
    """
    types = get_types()
    return render_template('error_handler.html', types=types, code=error.code,
                           name=error.name, description=error.description,
                           message="Ошибка на стороне сервера.")


@login_manager.user_loader
def load_user(user_id):
    """
    Log in user from database.

    :return: Database user by id
    """
    db_sess = create_session()  # Create database session
    user = db_sess.query(User).get(user_id)  # Get user by id from database
    db_sess.close()  # Shut down database session
    return user


def main():
    """Core of the program, starts the server."""
    # This part is needed to run server on heroku:
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)

    # If you want to run server on ngrok or local server use this:
    app.run()


# Protects users from accidentally invoking the script:
if __name__ == '__main__':
    main()
