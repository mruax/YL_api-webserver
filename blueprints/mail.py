# Import randint to generate mail code:
from random import randint

# Import dotenv to parse .env file:
from dotenv import load_dotenv
# Flask functions import:
from flask import render_template, request, Blueprint, redirect, abort
from flask_login import current_user

# Import mail functions:
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired

from data.mail_sender import send_mail
# Database functions import:
from data.db_session import create_session
from data.types import Type

# Parse .env file and load all mail variables:
from data.users import User

load_dotenv()

# This blueprint describes mail page:
mail_blueprint = Blueprint(
    'mail_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


def get_types():
    """
    Get item types from database.

    :return: List of item types
    """
    db_sess = create_session()  # Create database session
    types = db_sess.query(Type).all()  # Get item types from database
    db_sess.close()  # Shut down database session
    return types


class MailForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Отправить письмо')


class MailCodeForm(FlaskForm):
    code = IntegerField('Код', validators=[DataRequired()])
    submit = SubmitField('Проверить')


@mail_blueprint.route('/work', methods=["GET"])
def get_form():
    """
    Mail page.

    :return: HTML page with appropriate code
    """
    db_sess = create_session()  # Create database session
    user = db_sess.query(User).filter(User.email == current_user.email).all()
    db_sess.close()  # Shut down database session
    return render_template('mail_me.html', types=get_types(), form=MailForm(),
                           permission=user[0].permissions)


@mail_blueprint.route('/work', methods=["POST"])
def post_form():
    """
    Mail send.

    :return: HTML page with appropriate code
    """
    global mail_code
    mail_code = randint(100000, 999999)
    form = MailForm()
    email = request.values.get('email')
    if email == current_user.email and form.validate_on_submit():
        try:
            send_mail(email, 'Подтверждение электронного адреса',
                  f'Привет! Для того, чтобы получить доступ ко всем функциям '
                  f'необходимо ввести на сайте пароль: '
                  f'{mail_code} '
                  f'Вы можете ознакомиться с пользовательским соглашением в '
                  f'прикрепленном файле. '
                  f'Благодарим за использование нашего сервиса!',
                  ['static\\content\\terms_of_use.pdf'])
            return redirect('/check')
        except Exception as error:
            return render_template('error_handler.html', types=get_types(),
                                   code="520", name="Unknown Error",
                                   description=error,
                                   message=f"Во время отправки письма на "
                                           f"{email} возникла ошибка.")
    else:
        return render_template('error_handler.html', types=get_types(),
                               code="400", name="Bad Request",
                               description="Users email doesn't match the "
                                           "entered one.",
                               message="Введенная почта должна совпадать с "
                                       "почтой аккаунта.")


@mail_blueprint.route('/check', methods=["GET"])
def get_code_form():
    """
    Check mail code page.

    :return: HTML page with appropriate code
    """
    code_form = MailCodeForm()
    return render_template('check_mail_code.html', types=get_types(),
                           code="200", name="OK", code_form=code_form,
                           description="Email sent successfully.",
                           message=f"Письмо отправлено успешно.")


@mail_blueprint.route('/check', methods=["POST"])
def post_code_form():
    """
    Verify mail code.

    :return: HTML page with appropriate code
    """
    global mail_code
    code_form = MailCodeForm()
    code = request.values.get('code')
    if int(code) == mail_code:
        db_sess = create_session()  # Create database session
        user = db_sess.query(User).filter(User.email == current_user.email).first()
        if user:
            user.permissions = "cooperator"
            db_sess.commit()
            db_sess.close()  # Shut down database session
            return redirect('/work')
        abort(404)
    else:
        return render_template('error_handler.html', types=get_types(),
                               code="400", name="Bad Request",
                               description="Mail code doesn't match the "
                                           "entered one.",
                               message="Введенный код должен совпадать с "
                                       "кодом на вашей почте.")