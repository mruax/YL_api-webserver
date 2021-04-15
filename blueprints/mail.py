# Import randint to generate mail code:
from random import randint

# Import dotenv to parse .env file:
from dotenv import load_dotenv
# Flask import:
from flask import render_template, request, Blueprint

# Import blueprints:
from blueprints.mail_sender import send_mail

# Parse a .env file and load all mail variables:
load_dotenv()

# This blueprint describes mail page:
mail_blueprint = Blueprint(
    'mail_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


# Mail page:
@mail_blueprint.route('/mail', methods=["GET"])
def get_form():
    return render_template('mail_me.html')


# Mail send:
@mail_blueprint.route('/mail', methods=["POST"])
def post_form():
    email = request.values.get('email')
    try:
        send_mail(email, 'Подтверждение электронного адреса',
                  f'Привет! Для того, чтобы получить доступ к функциям разработчика необходимо ввести на сайте пароль: '
                  f'{randint(100000, 999999)} '
                  f'Вы можете ознакомиться с пользовательским соглашением в прикрепленном файле. Благодарим за использование нашего сервиса!',
                  ['static\\content\\terms_of_use.pdf'])
        return f"Письмо отправлено успешно на адрес {email}."
    except Exception as e:
        return f"Во время отправки письма на {email} возникла ошибка. {e}"
