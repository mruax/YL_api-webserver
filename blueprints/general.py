# Flask import:
from flask import Blueprint, render_template

# Database functions import:
from data import db_session
from data.types import Type

# This blueprint describes main page:
general_blueprint = Blueprint(
    'general_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


# Main page:
@general_blueprint.route('/')
def main_page():
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    return render_template('main_page.html', types=types)
