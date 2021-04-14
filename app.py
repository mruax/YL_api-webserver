# Flask import:
from flask import Flask, jsonify, make_response
from flask_login import LoginManager

import os

# Blueprints import:
from blueprints.auth import auth_blueprint
from blueprints.general import general_blueprint
from blueprints.products import products_blueprint
# Database functions import:
from data import db_session
from data.db_session import create_session
from data.users import User

# App initialization:
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('instance.config')
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)

# Blueprints registration:
app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(products_blueprint)


# Unknown page error handler:
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Unauthorized error handler:
@app.login_manager.unauthorized_handler
def unauth_handler():
    return make_response(jsonify(success=False,
                   data={'login_required': True},
                   message='Authorize please to access this page'), 401)

# Internal server error handler:
@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)


# Log in user from database:
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    global db_sess
    db_session.global_init("db/storage.db")
    db_sess = create_session()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
