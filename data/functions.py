import datetime
from data.diary import Diary
from data.user import User
from data.user_data import UserData
from data.user_login_data import UserLoginData
import uuid
from flask_login import current_user
from data import db_session


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
    db_sess.close()

    return user, user_data, user_login_data


def new_diary(brief_notes, sleep_start, sleep_end, sleep_imagination, condition_before, condition_after,
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

    db_sess = db_session.create_session()
    db_sess.add(diary)
    db_sess.commit()
    db_sess.close()

    return diary
