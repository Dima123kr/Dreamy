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
