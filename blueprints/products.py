# Flask import:
from flask import Blueprint, render_template
from flask_login import login_required

# Database functions import
from data import db_session
from data.types import Type

# This blueprint describes storage items pages:
products_blueprint = Blueprint(
    'products_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


# Storage items page:
@products_blueprint.route('/storage')
@products_blueprint.route('/storage/<string:display_type>')
@login_required
def storage_page(display_type="cards"):
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    # Groups item types by 3 in row:
    grouped_types = [types[i:i + 3] for i in range(0, len(types), 3)]
    # items = db_sess.query(Item).all()
    # companies = db_sess.query(Company).all()
    if display_type != "cards" and display_type != "list":
        display_type = "cards"
    return render_template(f'storage_{display_type}.html', title='Склад',
                           display_type=display_type,
                           grouped_types=grouped_types)
