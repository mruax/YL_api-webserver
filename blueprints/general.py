from flask import Blueprint, render_template

# This blueprint describes main page:
general_blueprint = Blueprint(
    'general_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')

@general_blueprint.route('/')
def main_page():
    return render_template('main_page.html')