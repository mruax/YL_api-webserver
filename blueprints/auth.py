# Flask import:
from flask import Blueprint, render_template, redirect
from flask_login import login_user, login_required, logout_user

# Database session import:
from data.db_session import create_session
from data.types import Type
from data.users import User
# Import login/register forms:
from forms.login import LoginForm
from forms.user import RegisterForm

# This blueprint describes sign in/sign up/logout pages:
auth_blueprint = Blueprint(
    'auth_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def reqister():
    """
    Registration page.

    :return: HTML page with appropriate code
    """
    form = RegisterForm()
    db_sess = create_session()
    types = db_sess.query(Type).all()
    if form.validate_on_submit():
        message = ""
        if form.password.data != form.password_again.data:
            message = "Пароли не совпадают"
        if db_sess.query(User).filter(User.email == form.email.data).first():
            message = "Такой email уже зарегистрирован"
        if db_sess.query(User).filter(User.login == form.login.data).first():
            message = "Такой login уже используется"
        if message:
            return render_template('register.html', title='Регистрация',
                                   form=form, types=types,
                                   message=message)
        user = User(
            login=form.login.data,
            email=form.email.data,
            permissions="user"
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           types=types)


# Login page:
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_sess = create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    types = db_sess.query(Type).all()
    return render_template('login.html', title='Авторизация', form=form,
                           types=types)


# Logout function:
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
