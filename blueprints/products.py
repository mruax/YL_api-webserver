# Flask functions import:
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

# Database functions import
from data.companies import Company
from data.db_session import create_session
from data.items import Item
from data.types import Type
from data.users import User
# This blueprint describes storage pages:
from forms.company import CompanyForm
from forms.item import ItemForm


from datetime import date

from forms.type import TypeForm

products_blueprint = Blueprint(
    'products_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')

# This var describes the page output form of storage items:
display_type = "cards"  # cards(default) or list


def correct_creation(types, message):
    return render_template('object_created.html', types=types, code="200", name="OK",
                           message=message, description="Object created")


def check_grammar(form):
    message = ""
    try:
        a = int(form.name.data)
        message = "Название указано неверно"
    except Exception:
        pass
    try:
        a = int(form.description.data)
        message = "Описание указано неверно"
    except Exception:
        pass
    return message


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
        items = db_sess.query(Item).all()  # Get all items from database
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
        companies = db_sess.query(Company).all()  # Get companies from database
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
    if request.method == 'POST':
        change_view()
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
    if request.method == 'POST':
        change_view()
    types, _ = get_types_extended()
    items, grouped_items = get_items_extended(item_type)
    companies, _ = get_companies_extended()
    return render_template(f'storage_items.html',
                           title=item_type, display_type=display_type,
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
    if request.method == 'POST':
        change_view()
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
    if request.method == 'POST':
        change_view()
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


@products_blueprint.route('/create/<string:object_name>',
                          methods=['GET', 'POST'])
@login_required
def create_object_page(object_name=""):
    """
    Create item/type of item/company page.

    :param object_name: Requested object to create
    :type object_name: str
    :return: HTML page with appropriate code
    """
    item_form = ItemForm()
    type_form = TypeForm()
    company_form = CompanyForm()

    types, _ = get_types_extended()

    if item_form.validate_on_submit():
        if object_name == "item":
            db_sess = create_session()  # Create database session
            company = db_sess.query(Company).filter(
                Company.name == item_form.company.data).first()
            item_type = db_sess.query(Type).filter(
                Type.name == item_form.item_type.data).first()
            db_sess.close()  # Shut down database session
            message = ""
            if not company:
                message = "Название компании указано неверно"
            if not item_type:
                message = "Тип товара указан неверно"
            try:
                if int(item_form.amount.data) < 0:
                    message = "Количество товара должно быть больше ноля"
            except Exception:
                message = "Количество товара указано неверно"
            if message == "":
                message = check_grammar(item_form)
            if message:
                return render_template('create_item.html', types=types,
                                       form=item_form,
                                       message=message)
            db_sess = create_session()  # Create database session
            item = Item()
            item.name = item_form.name.data
            item.description = item_form.description.data
            item.amount = item_form.amount.data
            item.company = item_form.company.data
            item.type = item_form.item_type.data
            item.creator = current_user.login
            item.date = date.today()
            db_sess.merge(item)
            db_sess.commit()
            db_sess.close()  # Shut down database session
            return correct_creation(types, message)
    if type_form.validate_on_submit():
        if object_name == "type":
            message = check_grammar(type_form)
            if message:
                return render_template('create_type.html', types=types,
                                       form=type_form,
                                       message=message)
            db_sess = create_session()  # Create database session
            item_type = Type()
            item_type.name = type_form.name.data
            item_type.description = type_form.description.data
            item_type.creator = current_user.login
            db_sess.merge(item_type)
            db_sess.commit()
            db_sess.close()  # Shut down database session
            return correct_creation(types, message)
    if company_form.validate_on_submit():
        if object_name == "company":
            message = check_grammar(company_form)
            try:
                if 100000 > int(company_form.post_address.data) > 999999:
                    message = "Почтовый индекс должен быть в формате XXXXXX"
            except Exception:
                message = "Почтовый индекс указан неверно"
            try:
                a = int(company_form.ORGN.data)
                if len(str(company_form.ORGN.data)) != 13:
                    message = "Введенный ОРГН не содержит 13 цифр"
            except Exception:
                message = "ОРГН должен содержать 13 цифр"
            try:
                a = int(company_form.OKPO.data)
                if len(str(company_form.OKPO.data)) != 10:
                    message = "Введенный ОКПО не содержит 10 цифр"
            except Exception:
                message = "ОКПО должен содержать 10 цифр"
            try:
                a = int(company_form.KPP.data)
                if len(str(company_form.KPP.data)) > 50:
                    message = "Введенный КПП не содержит 1-50 цифр"
            except Exception:
                message = "КПП должен содержать 1-50 цифр"
            try:
                a = int(company_form.INN.data)
                if len(str(company_form.INN.data)) != 12:
                    message = "Введенный ИНН не содержит 12 цифр"
            except Exception:
                message = "ИНН должен содержать 12 цифр"
            if message:
                return render_template('create_company.html', types=types,
                                       form=company_form,
                                       message=message)
            company = Company()
            company.name = company_form.name.data
            company.description = company_form.description.data
            company.address = company_form.address.data
            company.post_address = company_form.post_address.data
            company.phone_number = company_form.phone_number.data
            company.INN = company_form.INN.data
            company.KPP = company_form.KPP.data
            company.OKPO = company_form.OKPO.data
            company.ORGN = company_form.ORGN.data
            company.creator = current_user.login
            try:
                db_sess = create_session()  # Create database session
                db_sess.merge(company)
                db_sess.commit()
                db_sess.close()  # Shut down database session
                return correct_creation(types, "Успех")
            except Exception:
                return render_template('error_handler.html', types=types,
                                       code="400", name="Bad Request",
                                       description="The entered data already "
                                                   "exists in database",
                                       message="Какие-то из введённых данных "
                                               "уже существуют в базе данных.")
    form_out = ""
    if object_name == "company":
        form_out = company_form
    if object_name == "type":
        form_out = type_form
    if object_name == "item":
        form_out = item_form
    return render_template(f'create_{object_name}.html', title='Компания',
                           types=types, form=form_out)
