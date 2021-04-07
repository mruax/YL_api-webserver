import os
from urllib import request

from flask import Flask, Blueprint, render_template, url_for, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# TODO: разница между blueprint и app.route
# TODO: расширенная база данных


# blueprint = Blueprint(
#     'storage_api',
#     __name__,
#     template_folder='templates'
# )


@app.route('/register', methods=['POST', 'GET'])
def register():
    request.form.get('accept')
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
                            <title>Пример формы</title>
                            
                          </head>
                          <body>
                            <h1 align="center">Регистрация</h1>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                    <input type="login" class="form-control" id="login" placeholder="Введите логин" name="login">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <input type="password" class="form-control" id="password_repeat" placeholder="Повторите пароль" name="password_repeat">
                                    </br>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        # f.save(f"{os.path.dirname(os.path.abspath(__file__))}\\static\\img\\members_images\\{request.form['name']}_{request.form['surname']}.jpg")
        return redirect('http://127.0.0.1:8080')


# @blueprint.route('/')
@app.route('/')
def get_cell():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')