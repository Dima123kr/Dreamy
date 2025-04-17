import telebot
from telebot import types
from data.functions import new_diary
from data.db_session import global_init
from data.user_login_data import UserLoginData
from data import db_session
import datetime
import time

token = '7455913390:AAFIE_Zm8YDnDKwhEO647GJcmAUBx0ko9UM'
bot = telebot.TeleBot(token)

db_file = 'db/db.db'
global_init(db_file)

user_is_authorised = False
user = None


def item4(message):
    if not user_is_authorised:
        bot.send_message(
            message.chat.id, 'Введите почту:')
        bot.register_next_step_handler(message, user_loginem)
    else:
        bot.send_message(
            message.chat.id, 'Вы уже авторизованы')


def item3(message):
    if user_is_authorised:
        bot.send_message(
            message.chat.id, f'''Вы авторизованы под логином: {given_email}''')
    else:
        bot.send_message(
            message.chat.id, 'Вы не авторизованы')


def logus(message):
    global user_is_authorised
    user_is_authorised = True
    bot.send_message(
        message.chat.id, 'Вы успешно авторизованы')


def user_loginem(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global given_email
    global user
    given_email = message.text
    db_sess = db_session.create_session()
    user = db_sess.query(UserLoginData).filter(UserLoginData.email == given_email).first()
    print(user)
    if user is not None:
        user_loginpass(message)
    else:
        bot.send_message(
            message.chat.id, 'Такой почты не существует')


def user_loginpass(message):
    bot.send_message(
        message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, user_loginpass_body)


def user_loginpass_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    given_password = message.text
    if user.check_password(given_password):
        logus(message)

    else:
        bot.send_message(
            message.chat.id, 'Неверная почта или пароль')


def item5(message):
    global user_is_authorised
    user_is_authorised = False
    bot.send_message(
        message.chat.id, 'Вы вышли из аккаунта')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = types.KeyboardButton('Общая информация по восстановлению сна')
    item2 = types.KeyboardButton('Внести данные о сне')
    item3 = types.KeyboardButton('Мой аккаунт')
    item4 = types.KeyboardButton('Логин')
    item5 = types.KeyboardButton('Выход из аккаунта')
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}! Этот бот создан для улучшения твоего здоровья, а именно восстановления '
                     'твоего режима.\n\nЭтот проект поможет тебе улучшить качество сна, начать высыпаться, что '
                     'способствует улучшению твоего здоровья.\n\nИз функций ты сможешь следить за своей статистикой, '
                     'бот будет давать тебе советы, напоминать о то, что тебе нужно готовиться ко сну и т.д.\n\nУ вас '
                     'все получится, верьте в себя!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
    elif message.text == 'Логин':
        item4(message)
    elif message.text == 'Мой аккаунт':
        item3(message)
    elif message.text == 'Выход из аккаунта':
        item5(message)
    else:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите запрос заново')


def question1(message):
    bot.send_message(
        message.chat.id, 'Во сколько вы ложитесь спать? Ответ напишите в формате XX:XX')
    bot.register_next_step_handler(message, question1_body)


def question1_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global sleep_start
    try:
        if len((a := message.text.split(':'))) == 2 and all([i.isdigit() and int(i) >= 0 for i in a]):
            sleep_start = datetime.time(hour=int(a[0]), minute=int(a[1]))
            print(sleep_start)
            question2(message)
        else:
            bot.send_message(
                message.chat.id, 'Неверный формат. Введите ответ заново')
            question1(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question1(message)


def question2(message):
    bot.send_message(
        message.chat.id, 'Во сколько вы встаете? Ответ напишите в формате XX:XX')
    bot.register_next_step_handler(message, question2_body)


def question2_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global sleep_end
    try:
        if len((a := message.text.split(':'))) == 2 and all([i.isdigit() and int(i) >= 0 for i in a]):
            sleep_end = datetime.time(hour=int(a[0]), minute=int(a[1]))
            print(sleep_end)
            question3(message)
        else:
            bot.send_message(
                message.chat.id, 'Неверный формат. Введите ответ заново')
            question2(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question2(message)


def question3(message):
    bot.send_message(
        message.chat.id, 'Напишите краткие заметки по поводу вашего сна через запятую (если есть)')
    bot.register_next_step_handler(message, question3_body)


def question3_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global brief_notes
    brief_notes = message.text.strip()
    question4(message)


def question4(message):
    bot.send_message(
        message.chat.id, 'Напишите содержание своего сна (если был)')
    bot.register_next_step_handler(message, question4_body)


def question4_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global sleep_imagination
    sleep_imagination = message.text.strip()
    question5(message)


def question5(message):
    bot.send_message(
        message.chat.id, 'Как вы ощущали себя перед сном? (1/10)')
    bot.register_next_step_handler(message, question5_body)


def question5_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global condition_before
    try:
        if 0 < (a := int(message.text.strip())) <= 10:
            condition_before = a
            question6(message)
        else:
            bot.send_message(
                message.chat.id, 'Неверный формат. Введите ответ заново')
            question5(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question5(message)


def question6(message):
    bot.send_message(
        message.chat.id, 'Как вы ощущали себя после сна? (1/10)')
    bot.register_next_step_handler(message, question6_body)


def question6_body(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
        return
    elif message.text == 'Внести данные о сне':
        if user_is_authorised:
            question1(message)
            return
        else:
            bot.send_message(message.chat.id, 'Необходима авторизация')
            return
    elif message.text == 'Логин':
        item4(message)
        return
    elif message.text == 'Мой аккаунт':
        item3(message)
        return
    global condition_after
    try:
        if 1 <= (a := int(message.text.strip())) <= 10:
            condition_after = a
            answers_end(message)
        else:
            bot.send_message(
                message.chat.id, 'Неверный формат. Введите ответ заново')
            question6(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question6(message)


def answers_end(message):
    new_diary(brief_notes, sleep_start, sleep_end, sleep_imagination, condition_before, condition_after, user=user)
    end = types.InlineKeyboardMarkup(row_width=2)
    bot.send_message(
        message.chat.id, 'Вы успешно прошли все вопросы', reply_markup=end)


def item1(message):
    bot.send_message(message.chat.id,
                     '1. Соблюдайте режим:\nИдеальный сон длится где-то от 7 до 9 часов. Не стоит дремать ближе к '
                     'вечеру т.к это просто собьет сон(отменит желание и возможность заснуть в нужное время.\n\n'
                     '2. Перед сном кушайте в меру:\nЕшьте на ужин продукты, богатые калием и магнием - они известны, '
                     'как успокоители нервной системы. Не стоит переедать, но и не надо ложиться голодным. Ещё не '
                     'стоит пить напитки с кофеином перед сном.\n\n3. Отказаться от гаджетов:\nСтоит за час до сна '
                     'отказаться от гаджетов(вы можете не уследить за временем и сбить свой режим). На это есть '
                     'причина: мерцание гаджетов негативно влияет на нервную систему.\n\n4. Подготовка ко сну:\nПрежде '
                     'чем ложиться спать, стоит проветрить комну. Если день был невным, стоит принять горяую ванну.')


bot.infinity_polling()
