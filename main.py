import datetime
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.diary import Diary
from data.user import User
from data.user_data import UserData
from data.user_login_data import UserLoginData
from data.message import Message
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.edit import EditForm
from forms.diary import DiaryForm
from data.functions import new_user, new_diary, new_message
from openai import OpenAI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skjdgbrsgbntrsgkrnstrbnrstuiggbnrukitgghkutghearkghsejkvbseuyrsbgmfbv'
login_manager = LoginManager()
login_manager.init_app(app)

client = OpenAI(
    api_key="sk-xt9RThws4bABz9WdAh8NuKg6m5ujRrEm",
    base_url="https://api.proxyapi.ru/openai/v1"
)


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
            if user.check_password(form.password.data):
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
    diary = db_sess.query(Diary).filter(Diary.user == current_user.uuid and (datetime.date.today() - Diary.day).days <= 365).all()

    day_now = datetime.date.today().day
    month_now = datetime.date.today().month
    year_now = datetime.date.today().year
    day1 = list(filter(lambda x: x.day == datetime.date.today(), diary))
    if len(day1) == 0:
        day1 = [None]
    days = [day1[0]]
    if day_now >= 7:
        day_now_ = 7
    else:
        day_now_ = day_now
    for i in range(day_now_):
        day = list(filter(lambda x: x.day.day == day_now - i and x.day.month == month_now and
                                          x.day.year == year_now, diary))
        if len(day) == 0:
            day = [None]
        days.append(day[0])
    if month_now == 3:
        if year_now % 4 == 0:
            new_day = 29
        else:
            new_day = 28
    elif month_now in [2, 4, 6, 8, 9, 11, 1]:
            new_day = 31
    else:
        new_day = 30
    if month_now == 1:
        new_year = 1
    else:
        new_year = 0
    for i in range(7 - day_now_):
        day = list(filter(lambda x: x.day.day == new_day - i and x.day.month == month_now - 1 and
                                          x.day.year == year_now - new_year, diary))
        if len(day) == 0:
            day = [None]
        days.append(day[0])
    days = list(reversed(days))
    day_sleep_length = []
    day_sleep_start = []
    day_sleep_end = []
    day_condition_delta = []
    day_condition_before = []
    day_condition_after = []
    for i in days:
        if not i:
            day_sleep_start.append(0)
            day_sleep_end.append(0)
            day_condition_delta.append(0)
            day_condition_before.append(0)
            day_condition_after.append(0)
            day_sleep_length.append(0)
            continue
        if i.sleep_start > i.sleep_end:
            day_sleep_length.append(
                (datetime.timedelta(0, 0, 0, 0, i.sleep_end.minute, i.sleep_end.hour) +
                 datetime.timedelta(0, 0, 0, 0, 0, 24) -
                 datetime.timedelta(0, 0, 0, 0,
                                    i.sleep_start.minute, i.sleep_start.hour)).seconds / 3600)
        else:
            day_sleep_length.append(
                (datetime.timedelta(0, 0, 0, 0, i.sleep_end.minute, i.sleep_end.hour) -
                 datetime.timedelta(0, 0, 0, 0,
                                    i.sleep_start.minute, i.sleep_start.hour)).seconds / 3600)

        day_sleep_start.append(i.sleep_start.hour + i.sleep_start.minute / 60)
        day_sleep_end.append(i.sleep_end.hour + i.sleep_end.minute / 60)
        day_condition_delta.append(i.condition_after - i.condition_before)
        day_condition_before.append(i.condition_before)
        day_condition_after.append(i.condition_after)

    month_now = datetime.date.today().month
    year_now = datetime.date.today().year
    months = [list(filter(lambda x: x.day.month == month_now, diary))]
    for i in range(month_now - 1):
        months.append(list(filter(lambda x: x.day.month == month_now - i - 1 and year_now == x.day.year, diary)))
    for i in range(12 - month_now):
        months.append(list(filter(lambda x: x.day.month == 12 - i and year_now - 1 == x.day.year, diary)))
    months = list(reversed(months))
    month_sleep_length = []
    month_sleep_start = []
    month_sleep_end = []
    month_condition_delta = []
    month_condition_before = []
    month_condition_after = []
    for i in months:
        if len(i) == 0:
            month_sleep_start.append(0)
            month_sleep_end.append(0)
            month_condition_delta.append(0)
            month_condition_before.append(0)
            month_condition_after.append(0)
            month_sleep_length.append(0)
            continue
        sleep_start_list = []
        sleep_end_list = []
        condition_before_list = []
        condition_after_list = []
        for n in i:
            sleep_start_list.append(datetime.timedelta(0, 0, 0, 0, n.sleep_start.minute, n.sleep_start.hour).seconds / 3600)
            sleep_end_list.append(datetime.timedelta(0, 0, 0, 0, n.sleep_end.minute, n.sleep_end.hour).seconds / 3600)
            condition_before_list.append(n.condition_before)
            condition_after_list.append(n.condition_after)
        sleep_start = sum(sleep_start_list) / len(sleep_start_list)
        sleep_end = sum(sleep_end_list) / len(sleep_end_list)
        condition_before = sum(condition_before_list) / len(condition_before_list)
        condition_after = sum(condition_after_list) / len(condition_after_list)
        if sleep_start > sleep_end:
            month_sleep_length.append(sleep_end + 24 - sleep_start)
        else:
            month_sleep_length.append(sleep_end - sleep_start)
        month_sleep_start.append(sleep_start)
        month_sleep_end.append(sleep_end)
        month_condition_delta.append(condition_after - condition_before)
        month_condition_before.append(condition_before)
        month_condition_after.append(condition_after)

    diary_ = [
        " ".join(list(map(str, day_sleep_length))),     " ".join(list(map(str, month_sleep_length))),
        " ".join(list(map(str, day_sleep_start))),      " ".join(list(map(str, month_sleep_start))),
        " ".join(list(map(str, day_sleep_end))),        " ".join(list(map(str, month_sleep_end))),
        " ".join(list(map(str, day_condition_delta))),  " ".join(list(map(str, month_condition_delta))),
        " ".join(list(map(str, day_condition_before))), " ".join(list(map(str, month_condition_before))),
        " ".join(list(map(str, day_condition_after))),  " ".join(list(map(str, month_condition_after)))
    ]
    return render_template('account.html', db_session=db_session, diary=",".join(diary_))


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


@app.route("/diary_start")
@login_required
def diary_start():
    db_sess = db_session.create_session()
    is_completed = len(db_sess.query(Diary).filter(Diary.day == datetime.date.today(), Diary.user == current_user.uuid).all()) > 0
    return render_template("diary_start.html", date=datetime.date.today(), is_completed=is_completed)


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    db_sess = db_session.create_session()
    if len(db_sess.query(Diary).filter(Diary.day == datetime.date.today(), Diary.user == current_user.uuid).all()) > 0:
        return redirect("/")
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
        return redirect("/")
    return render_template("diary.html", date=datetime.date.today(), form=form)


@app.route('/chat_gpt', methods=['GET', 'POST'])
@login_required
def chat_gpt():
    if request.method == "POST":
        try:
            new_message(request.form["message"])
        except Exception as err:
            db_sess = db_session.create_session()
            messages = db_sess.query(Message).filter(Message.user == current_user.uuid).all()
            for i in messages:
                db_sess.delete(i)
            db_sess.commit()
    db_sess = db_session.create_session()
    messages = db_sess.query(Message).filter(Message.user == current_user.uuid).all()
    return render_template("chat_gpt.html", title="ChatGPT", messages=messages)


if __name__ == "__main__":
    db_session.global_init("db/db.db")
    app.run(host='127.0.0.1', port='8888', debug=False)
