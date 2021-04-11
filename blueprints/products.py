# Flask import:
from flask import Blueprint, render_template, request
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

# This var describes the page output form of storage items:
display_type = "cards"  # or list

# Storage item types page:
@products_blueprint.route('/storage', methods=['GET', 'POST'])
# @products_blueprint.route('/storage/<string:display_type>')
@login_required
def storage_item_types_page():
    global display_type
    if request.method == 'POST':
        if display_type == "cards":
            display_type = "list"
        else:
            display_type = "cards"
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    # Groups item types by 3 in row:
    grouped_types = [types[i:i + 3] for i in range(0, len(types), 3)]
    return render_template(f'storage_item_types.html', title='Склад',
                           display_type=display_type,
                           types=types,
                           grouped_types=grouped_types)


# Storage items page:
@products_blueprint.route('/storage/<string:item_type>')
@products_blueprint.route('/storage/<string:item_type>/<string:display_type>')
@login_required
def storage_items_page(item_type="", display_type="cards"):
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
                           types=types,
                           grouped_types=grouped_types)
