# Flask import:
from flask import Flask, jsonify, make_response
from flask_login import LoginManager
from flask_ngrok import run_with_ngrok

# Blueprints import:
from blueprints.auth import auth_blueprint
from blueprints.general import general_blueprint
# Database session import:
from data import db_session
from data.db_session import create_session

# App initialization:
app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Blueprints registration:
app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint)


# Unknown page error handler:
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    global db_sess
    db_session.global_init("db/storage.db")
    db_sess = create_session()
    app.run()


if __name__ == '__main__':
    main()
