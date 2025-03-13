import datetime
import os
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.diary import Diary
from data.user import User
from data.user_data import UserData
from data.user_login_data import UserLoginData
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.edit import EditForm
from forms.diary import DiaryForm
from data.functions import new_user, new_diary

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skjdgbrsgbntrsgkrnstrbnrstuiggbnrukitgghkutghearkghsejkvbseuyrsbgmfbv'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    return user


@app.route('/')
def main():
    return render_template('main.html', title="Dreamy")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    db_sess = db_session.create_session()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        if db_sess.query(UserData).filter(UserData.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Указанная почта занята")
        if not 14 < datetime.date.today().year - form.date_of_birthday.data.year < 200:
            return render_template('register.html', title='Регистрация', form=form, message="Недопустимый возраст")
        users = new_user(form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.gender.data,
                        form.date_of_birthday.data)
        user = users[0]
        db_sess.add(user)
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(UserLoginData).filter(UserLoginData.email == form.email.data).first()
        if user:
            if user.check_password:
                user_ = db_sess.query(User).filter(User.uuid == user.uuid).first()
                login_user(user_, remember=form.remember_me.data)
                return redirect("/")
            else:
                return render_template('login.html', message="Неправильный пароль", title='Авторизация', form=form)
        else:
            return render_template('login.html', message="Неправильный логин", title='Авторизация', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/account')
def account():
    db_sess = db_session.create_session()
    diary = db_sess.query(Diary).filter(Diary.user == current_user.uuid).all()
    diary_ = []
    for i in diary:
        diary_.append(f"{i.day} {i.sleep_start} {i.sleep_end} {i.condition_before} {i.condition_after}")
    diary_ = ",".join(diary_)
    return render_template('account.html', db_session=db_session, diary=diary_)


@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditForm()
    if request.method == "GET":
        form.first_name.data = current_user.get_data().first_name
        form.last_name.data = current_user.get_data().last_name
        form.email.data = current_user.get_data().email
        form.password.data = current_user.get_login_data().password
        form.password_again.data = current_user.get_login_data().password
        form.gender.data = current_user.get_data().gender
        form.date_of_birthday.data = current_user.get_data().date_of_birthday
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit.html', title='Изменение аккаунта', form=form, message="Пароли не совпадают")
        if not 14 < datetime.date.today().year - form.date_of_birthday.data.year < 200:
            return render_template('edit.html', title='Изменение аккаунта', form=form, message="Недопустимый возраст")
        db_sess = db_session.create_session()
        user_data = current_user.get_data(db_sess)
        user_login_data = current_user.get_login_data(db_sess)
        user_data.first_name = form.first_name.data
        user_data.last_name = form.last_name.data
        user_data.email = form.email.data
        user_login_data.email = form.email.data
        user_login_data.set_password(form.password.data)
        user_data.gender = form.gender.data
        user_data.date_of_birthday = form.date_of_birthday.data
        db_sess.add(user_data)
        db_sess.add(user_login_data)
        db_sess.commit()
        return redirect('/account')
    return render_template('edit.html', title='Изменение аккаунта', form=form)


@app.route('/account/delete')
@login_required
def delete_account():
    user = current_user
    user_data = user.get_data
    user_login_data = user.get_login_data
    db_sess = db_session.create_session()
    db_sess.delete(user)
    db_sess.delete(user_data)
    db_sess.delete(user_login_data)
    db_sess.commit()
    return redirect('/')


@app.route('/account/leave')
@login_required
def leave_account():
    logout_user()
    return redirect('/')


@app.route('/diary_start')
@login_required
def diary_start():
    db_sess = db_session.create_session()
    is_completed = len(db_sess.query(Diary).filter(Diary.day == datetime.date.today()).all()) > 0
    return render_template('diary_start.html', date=datetime.date.today(), is_completed=is_completed)


@app.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    form = DiaryForm()
    if form.validate_on_submit():
        diary = new_diary(
            form.brief_notes.data,
            form.sleep_start.data,
            form.sleep_end.data,
            form.sleep_imagination.data,
            form.condition_before.data,
            form.condition_after.data
        )
        db_sess = db_session.create_session()
        db_sess.add(diary)
        db_sess.commit()
        return redirect('/')
    return render_template('diary.html', date=datetime.date.today(), form=form)


@app.route('/beta', methods=['GET', 'POST'])
def beta():
    return render_template('beta.html')


if __name__ == "__main__":
    db_session.global_init("db/db.db")
    app.run(host='127.0.0.1', port='8888', debug=False)
