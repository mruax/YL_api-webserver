# Flask functions import:
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


@general_blueprint.route('/')
def main_page():
    """
    Main page content.

    :return: HTML page with appropriate code
    """
    db_sess = db_session.create_session()  # Create database session
    types = db_sess.query(Type).all()  # Get item types from database
    db_sess.close()  # Shut down database session
    return render_template('main_page.html', types=types)
