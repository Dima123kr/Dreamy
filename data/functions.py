import datetime
from data.diary import Diary
from data.user import User
from data.user_data import UserData
from data.user_login_data import UserLoginData
from data.message import Message
import uuid
from flask_login import current_user
from data import db_session
import markdown


def new_user(first_name, last_name, email, password, gender, date_of_birthday, is_admin=False, is_boss=False):
    if is_boss:
        is_admin = True

    user_uuid = uuid.uuid4()

    user = User()
    user.uuid = user_uuid

    user_data = UserData()
    user_data.uuid = user_uuid
    user_data.first_name = first_name
    user_data.last_name = last_name
    user_data.email = email
    user_data.gender = gender
    user_data.date_of_birthday = date_of_birthday
    user_data.is_admin = is_admin
    user_data.is_boss = is_boss

    user_login_data = UserLoginData()
    user_login_data.uuid = user_uuid
    user_login_data.set_password(password)
    user_login_data.email = email

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.add(user_data)
    db_sess.add(user_login_data)
    db_sess.commit()

    return user, user_data, user_login_data


def new_diary(brief_notes, sleep_start, sleep_end, sleep_imagination, condition_before, condition_after, result,
              user=current_user, day=datetime.date.today()):
    diary = Diary()
    diary.user = user.uuid
    diary.day = day
    diary.brief_notes = brief_notes
    diary.sleep_start = sleep_start
    diary.sleep_end = sleep_end
    diary.sleep_imagination = sleep_imagination
    diary.condition_before = condition_before
    diary.condition_after = condition_after
    diary.result = result

    db_sess = db_session.create_session()
    db_sess.add(diary)
    db_sess.commit()

    return diary


def new_message(message, user=current_user):
    if len(message.strip(" ")) != 0:
        from main import client
        db_sess = db_session.create_session()
        messages_db = db_sess.query(Message).filter(Message.user == user.uuid).all()
        messages = []
        for i in messages_db:
            if i.is_gpt:
                role = "assistant"
            else:
                role = "user"
            messages.append({
                "role": role,
                "content": i.message
            })
        messages.append({
            "role": "user",
            "content": message
        })
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
        )
        result = chat_completion.choices[0].message.content
        result = markdown.markdown(result)

        message_db1 = Message()
        message_db1.user = user.uuid
        message_db1.is_gpt = False
        message_db1.message = message

        message_db2 = Message()
        message_db2.user = user.uuid
        message_db2.is_gpt = True
        message_db2.message = result

        db_sess = db_session.create_session()
        db_sess.add(message_db1)
        db_sess.add(message_db2)
        db_sess.commit()

        return message_db1, message_db2
    return None


def get_statistics():
    db_sess = db_session.create_session()
    diary = db_sess.query(Diary).filter(
        Diary.user == current_user.uuid and (datetime.date.today() - Diary.day).days <= 365).all()
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
            sleep_start_list.append(
                datetime.timedelta(0, 0, 0, 0, n.sleep_start.minute, n.sleep_start.hour).seconds / 3600)
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

    return [
        day_sleep_length, month_sleep_length,
        day_sleep_start, month_sleep_start,
        day_sleep_end, month_sleep_end,
        day_condition_delta, month_condition_delta,
        day_condition_before, month_condition_before,
        day_condition_after, month_condition_after
    ]
