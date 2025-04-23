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
from data.functions import new_user, new_diary, new_message, get_statistics
from openai import OpenAI
import markdown

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
    diary_ = get_statistics()
    diary_ = [
        " ".join(list(map(str, diary_[0]))), " ".join(list(map(str, diary_[1]))),
        " ".join(list(map(str, diary_[2]))), " ".join(list(map(str, diary_[3]))),
        " ".join(list(map(str, diary_[4]))), " ".join(list(map(str, diary_[5]))),
        " ".join(list(map(str, diary_[6]))), " ".join(list(map(str, diary_[7]))),
        " ".join(list(map(str, diary_[8]))), " ".join(list(map(str, diary_[9]))),
        " ".join(list(map(str, diary_[10]))), " ".join(list(map(str, diary_[11])))
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
    if is_completed:
        db_sess = db_session.create_session()
        diary = db_sess.query(Diary).filter(Diary.user == current_user.uuid, Diary.day == datetime.date.today()).first()
        return render_template("diary_start.html", date=datetime.date.today(), is_completed=is_completed, diary=diary)
    else:
        return render_template("diary_start.html", date=datetime.date.today(), is_completed=is_completed)


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    db_sess = db_session.create_session()
    if len(db_sess.query(Diary).filter(Diary.day == datetime.date.today(), Diary.user == current_user.uuid).all()) > 0:
        return redirect("/")
    form = DiaryForm()
    if form.validate_on_submit():
        message = f'''
            Привет, представь, что ты эксперт по сну и тебе надо дать развернутый комментарий по сну, дать несколько 
            персональных советов, опираясь на следующую анкету:
            краткие заметки по сну: {form.brief_notes.data};
            время начала сна: {form.sleep_start.data};
            время окончания сна: {form.sleep_end.data};
            что приснилось: {form.sleep_imagination.data};
            как себя чувствовал перед сном от 1 до 10: {form.condition_before.data};
            как себя чувствовал после сна от 1 до 10: {form.condition_after.data}.
            После каждого блока со списком обязательно вставь какой нибудь текст.
        '''
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            model="gpt-4o",
        )
        result = chat_completion.choices[0].message.content
        result = markdown.markdown(result)

        diary = new_diary(
            form.brief_notes.data,
            form.sleep_start.data,
            form.sleep_end.data,
            form.sleep_imagination.data,
            form.condition_before.data,
            form.condition_after.data,
            result
        )

        diary_ = get_statistics()
        message = f'''
                    Привет, представь, что ты эксперт по сну и тебе надо дать развернутый комментарий по сну, дать 
                    несколько персональных советов, опираясь на следующие данные о сне за последнюю неделю по формату 
                    "Критерий-6 дней назад;5 дней назад;4 дня назад;3 дня назад;2 дня назад;1 день назад;сегодня.":
                    Начало сна-23:00;22:00;00:00;01:00;02:00;23:00;21:00.
                    Окончание сна-07:00;08:00;07:00;06:00;07:00;07:00;12:00.
                    Оценка состояния перед сном от 1 до 10-5;6;7;4;8;1;2.
                    Оценка состояния после сна от 1 до 10-9;8;9;1;7;9;10.
                    Также необходимо учесть средние данные за последние 12 месяцев(данные будут введены по формату 
                    "Критерий-11 месяцев назад;10 месяцев назад;9 месяцев назад;8 месяцев назад;7 месяцев назад;
                    6 месяцев назад;5 месяцев назад;4 месяца назад;3 месяца назад;2 месяца назад;1 месяц назад;
                    этот месяц."):
                    Начало сна-23:00;22:00;00:00;01:00;02:00;23:00;21:00;23:00;22:00;00:00;01:00;02:00.
                    Окончание сна-07:00;08:00;07:00;06:00;07:00;07:00;12:00;08:00;07:00;06:00;07:00;07:00.
                    Оценка состояния перед сном от 1 до 10-5;6;7;4;8;1;2;5;6;7;4;8.
                    Оценка состояния после сна от 1 до 10-9;8;9;1;7;9;10;9;1;7;9;10.
                    Также важно учесть то, что некоторые значения, равные нулю могут оказаться просто 
                    незаполненными полями.
                    Весь итоговый ответ по объему должен быть меньше 1000 слов.
                '''
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            model="gpt-4o",
        )
        result = chat_completion.choices[0].message.content
        result = markdown.markdown(result)
        user_data = db_sess.query(UserData).filter(UserData.uuid == current_user.uuid).first()
        user_data.recommendation = result

        db_sess.add(user_data)
        db_sess.add(diary)
        db_sess.commit()
        return redirect("/diary_start")
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
