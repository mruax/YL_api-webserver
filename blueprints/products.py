from flask import Blueprint, render_template

from flask_login import login_required

# This blueprint describes storage items pages:
products_blueprint = Blueprint(
    'products_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


# Storage items page:
@products_blueprint.route('/storage')
@login_required
def storage_page():
    return render_template('storage.html', title='Склад')
