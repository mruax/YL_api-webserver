# Import randint to generate mail code:
from random import randint

# Import dotenv to parse .env file:
from dotenv import load_dotenv
# Flask import:
from flask import render_template, request, Blueprint

# Import blueprints:
from blueprints.mail_sender import send_mail
# Database functions import:
from data import db_session
from data.types import Type

# Parse a .env file and load all mail variables:
load_dotenv()

# This blueprint describes mail page:
mail_blueprint = Blueprint(
    'mail_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


# Mail page:
@mail_blueprint.route('/work', methods=["GET"])
def get_form():
    db_sess = db_session.create_session()
    types = db_sess.query(Type).all()
    return render_template('mail_me.html', types=types)


# Mail send:
@mail_blueprint.route('/work', methods=["POST"])
def post_form():
    # TODO: the requested mail must be equal to users mail
    email = request.values.get('email')
    try:
        send_mail(email, 'Подтверждение электронного адреса',
                  f'Привет! Для того, чтобы получить доступ ко всем функциям необходимо ввести на сайте пароль: '
                  f'{randint(100000, 999999)} '
                  f'Вы можете ознакомиться с пользовательским соглашением в прикрепленном файле. Благодарим за использование нашего сервиса!',
                  ['static\\content\\terms_of_use.pdf'])
        return f"Письмо отправлено успешно на адрес {email}."
    except Exception as e:
        return f"Во время отправки письма на {email} возникла ошибка. {e}"
