from dotenv import load_dotenv
from flask import Flask, render_template, request

from random import randint
from mail.mail_sender import send_mail

app = Flask(__name__)
load_dotenv()


@app.route('/', methods=["GET"])
def get_form():
    return render_template('mail_me.html')


@app.route('/', methods=["POST"])
def post_form():
    email = request.values.get('email')
    try:
        send_mail(email, 'Подтверждение электронного адреса', f'Привет! Для того, чтобы получить доступ к функциям разработчика необходимо ввести на сайте пароль: '
                                                              f'{randint(100000,999999)} '
                                                              f'Вы можете ознакомиться с пользовательским соглашением в прикрепленном файле. Благодарим за использование нашего сервиса!',
                  ['content\\terms_of_use.pdf'])
        return f"Письмо отправлено успешно на адрес {email}."
    except Exception as e:
        return f"Во время отправки письма на {email} возникла ошибка. {e}"


if __name__ == "__main__":
    app.run()