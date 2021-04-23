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


def get_types():
    """
    Get item types from database.

    :return: List of item types
    """
    db_sess = create_session()  # Create database session
    types = db_sess.query(Type).all()  # Get item types from database
    db_sess.close()  # Shut down database session
    return types


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def reqister():
    """
    Registration page.

    :return: HTML page with appropriate code
    """
    form = RegisterForm()
    types = get_types()
    if form.validate_on_submit():
        db_sess = create_session()  # Create database session
        message = ""
        if form.password.data != form.password_again.data:
            message = "Пароли не совпадают"
        if db_sess.query(User).filter(User.email == form.email.data).first():
            message = "Такой email уже зарегистрирован"
        if db_sess.query(User).filter(User.login == form.login.data).first():
            message = "Такой login уже используется"
        if message:
            db_sess.close()  # Shut down database session
            return render_template('register.html', title='Регистрация',
                                   form=form, types=types, message=message)
        user = User(
            login=form.login.data,
            email=form.email.data,
            permissions="user"
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()  # Shut down database session
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           types=types)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page.

    :return: HTML page with appropriate code
    """
    form = LoginForm()
    types = get_types()
    if form.validate_on_submit():
        db_sess = create_session()  # Create database session
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        db_sess.close()  # Shut down database session
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', types=types, form=form,
                               message="Неправильный логин или пароль")
    return render_template('login.html', title='Авторизация', form=form,
                           types=types)


@auth_blueprint.route('/logout')
@login_required
def logout():
    """
    Logout function.

    :return: Redirect to main page
    """
    logout_user()
    return redirect("/")
