# Flask import:
from flask import Blueprint, render_template, request
from flask_login import login_required

# Database functions import
from data import db_session
from data.companies import Company
from data.items import Item
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
    # Group item types by 3 in row:
    grouped_types = [types[i:i + 3] for i in range(0, len(types), 3)]
    return render_template(f'storage_item_types.html', title='Категории товаров',
                           display_type=display_type,
                           types=types,
                           grouped_types=grouped_types)


# Storage items page:
@products_blueprint.route('/storage/<string:item_type>', methods=['GET', 'POST'])
@login_required
def storage_items_page(item_type=""):
    global display_type
    if request.method == 'POST':
        if display_type == "cards":
            display_type = "list"
        else:
            display_type = "cards"
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    items = db_sess.query(Item).filter(Item.type == item_type).all()
    companies = db_sess.query(Company).all()
    # Group items by 3 in row:
    grouped_items = [items[i:i + 3] for i in range(0, len(items), 3)]
    return render_template(f'storage_items.html',
                           title='Товары',
                           display_type=display_type,
                           types=types, items=items, companies=companies,
                           grouped_items=grouped_items)


# Storage companies page:
@products_blueprint.route('/companies', methods=['GET', 'POST'])
@login_required
def storage_companies_page():
    global display_type
    if request.method == 'POST':
        if display_type == "cards":
            display_type = "list"
        else:
            display_type = "cards"
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    companies = db_sess.query(Company).all()
    # Group companies by 3 in row:
    grouped_companies = [companies[i:i + 3] for i in range(0, len(companies), 3)]
    return render_template(f'storage_companies.html', title='Компании',
                           display_type=display_type,
                           types=types, companies=companies,
                           grouped_companies=grouped_companies)


# Storage company page:
@products_blueprint.route('/companies/<string:company_name>', methods=['GET', 'POST'])
@login_required
def storage_company_page(company_name=""):
    global display_type
    if request.method == 'POST':
        if display_type == "cards":
            display_type = "list"
        else:
            display_type = "cards"
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    company = db_sess.query(Company).filter(Company.name == company_name).first()
    items = db_sess.query(Item).filter(Item.company == company_name).all()
    # Group items by 3 in row:
    grouped_items = [items[i:i + 3] for i in range(0, len(items), 3)]
    return render_template(f'storage_company.html',
                           title='Компания',
                           display_type=display_type,
                           types=types, items=items, company=company,
                           grouped_items=grouped_items)