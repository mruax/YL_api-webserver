# Flask import:
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

# Database functions import
from data.companies import Company
from data.db_session import create_session
from data.items import Item
from data.types import Type

# This blueprint describes storage pages:
from data.users import User

products_blueprint = Blueprint(
    'products_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')

# This var describes the page output form of storage items:
display_type = "cards"  # cards(default) or list


def change_view():
    """Changes display type to the opposite."""
    global display_type
    if display_type == "cards":
        display_type = "list"
    else:
        display_type = "cards"


def get_types_extended():
    """
    Get item types from database and also group them by 3 in row.

    :return: List of item types
    """
    db_sess = create_session()  # Create database session
    types = db_sess.query(Type).all()  # Get item types from database
    db_sess.close()  # Shut down database session
    # Group item types by 3 in row:
    grouped_types = [types[i:i + 3] for i in range(0, len(types), 3)]
    return types, grouped_types


def get_items_extended(item_type="", company_name="", item_id=1):
    """
    Get items from database and also group them by 3 in row.

    :return: List of items
    """
    db_sess = create_session()  # Create database session
    if item_type:  # If item type specified
        items = db_sess.query(Item).filter(Item.type == item_type).all()
    elif company_name:  # If company name specified
        items = db_sess.query(Item).filter(Item.company == company_name).all()
    elif item_id:  # If item id specified
        items = db_sess.query(Item).filter(Item.id == item_id).all()
    else:
        items = db_sess.query(Item).all()  # Get items from database
    # Group items by 3 in row:
    grouped_items = [items[i:i + 3] for i in range(0, len(items), 3)]
    db_sess.close()  # Shut down database session
    return items, grouped_items


def get_companies_extended(company_name=""):
    """
    Get companies from database and also group them by 3 in row.

    :return: List of items
    """
    db_sess = create_session()  # Create database session
    if not company_name:  # If company name not specified
        companies = db_sess.query(Company).all()  # Get items from database
        # Group companies by 3 in row:
        grouped_companies = [companies[i:i + 3] for i in
                             range(0, len(companies), 3)]
    else:
        companies = db_sess.query(Company).filter(
            Company.name == company_name).first()
        grouped_companies = ""
    db_sess.close()  # Shut down database session
    return companies, grouped_companies


@products_blueprint.route('/storage', methods=['GET', 'POST'])
@login_required
def storage_item_types_page():
    """
    Storage item types page.

    :return: HTML page with appropriate code
    """
    global display_type
    if request.method == 'POST': change_view()
    types, grouped_types = get_types_extended()
    return render_template(f'storage_item_types.html', types=types,
                           title='Категории товаров',
                           display_type=display_type,
                           grouped_types=grouped_types)


@products_blueprint.route('/storage/<string:item_type>',
                          methods=['GET', 'POST'])
@login_required
def storage_items_page(item_type=""):
    """
    Storage items page.

    :param item_type: Requested item type
    :type item_type: str
    :return: HTML page with appropriate code
    """
    global display_type
    if request.method == 'POST': change_view()
    types, _ = get_types_extended()
    items, grouped_items = get_items_extended(item_type)
    companies, _ = get_companies_extended()
    return render_template(f'storage_items.html',
                           title='Товары',
                           display_type=display_type,
                           types=types, items=items, companies=companies,
                           grouped_items=grouped_items)


@products_blueprint.route('/storage/<string:item_type>/<int:item_id>',
                          methods=['GET', 'POST'])
@login_required
def storage_item_page(item_type="", item_id=1):
    """
    Storage item page.

    :param item_type: Requested item type
    :type item_type: str
    :param item_id: Requested item id
    :type item_id: int
    :return: HTML page with appropriate code
    """
    global display_type
    item, _ = get_items_extended(item_id=item_id)
    types, _ = get_types_extended()
    return render_template(f'storage_item.html',
                           title='Товар', display_type=display_type,
                           types=types, item=item[0], item_type=item_type)


@products_blueprint.route('/companies', methods=['GET', 'POST'])
@login_required
def storage_companies_page():
    """
    Storage companies page.

    :return: HTML page with appropriate code
    """
    global display_type
    if request.method == 'POST': change_view()
    types, _ = get_types_extended()
    companies, grouped_companies = get_companies_extended()
    return render_template(f'storage_companies.html', title='Компании',
                           display_type=display_type,
                           types=types, companies=companies,
                           grouped_companies=grouped_companies)


@products_blueprint.route('/companies/<string:company_name>',
                          methods=['GET', 'POST'])
@login_required
def storage_company_page(company_name=""):
    """
    Storage company page.

    :param company_name: Requested company name
    :type company_name: str
    :return: HTML page with appropriate code
    """
    global display_type
    if request.method == 'POST': change_view()
    items, grouped_items = get_items_extended(company_name=company_name)
    types, _ = get_types_extended()
    company, _ = get_companies_extended(company_name)
    return render_template(f'storage_company.html',
                           title='Компания',
                           display_type=display_type,
                           types=types, items=items, company=company,
                           grouped_items=grouped_items)


@products_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_page():
    """
    Create page content.

    :return: HTML page with appropriate code
    """
    types, _ = get_types_extended()
    db_sess = create_session()  # Create database session
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    db_sess.close()  # Shut down database session
    return render_template('create_menu.html', types=types,
                           permission=user.permissions)