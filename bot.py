import sqlite3
import telebot
from telebot import types
import datetime
import time

token = '7455913390:AAFIE_Zm8YDnDKwhEO647GJcmAUBx0ko9UM'
bot = telebot.TeleBot(token)

conn = sqlite3.connect('db/db.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user: str, answer1: str, answer2: str, answer3: int, answer4: int):
    cursor.execute('SELECT * FROM answer WHERE user = ?', (user,))
    result = cursor.fetchone()
    if result is not None:
        cursor.execute('UPDATE answer SET answer1 = ?, answer2 = ?, answer3 = ?, answer4 = ? WHERE user = ?', (answer1, answer2, answer3, answer4, user))
        conn.commit()
        return
    cursor.execute('INSERT INTO answer VALUES (?, ?, ?, ?, ?)', (user, answer1, answer2, answer3, answer4))
    conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = types.KeyboardButton('Общая информация по восстановлению сна')
    item2 = types.KeyboardButton('Начать путь к восстановлению режима')
    item3 = types.KeyboardButton('Внести данные сегодняшнего поддержания режима')
    item4 = types.KeyboardButton('Личная статистика')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Этот бот создан для улучшения твоего здоровья, а именно восстановления твоего режима.\n\nЭтот проект поможет тебе улучшить качество сна, начать высыпаться, что способствует улучшению твоего здоровья.\
        \n\nИз функций ты сможешь следить за своей статистикой, бот будет давать тебе советы, напоминать о то, что тебе нужно готовиться ко сну и т.д.\n\nУ вас все получится, верьте в себя!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Общая информация по восстановлению сна':
        item1(message)
    elif message.text == 'Начать путь к восстановлению режима':
        question1(message)
    else:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите запрос заново')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'analyze':
            bot.send_message(call.message.chat.id, "Анализирую данные")
            time.sleep(3)
            



def question1(message):
    bot.send_message(
        message.chat.id, 'Во сколько вы ложитесь спать? Ответ напишите в формате XX:XX')
    bot.register_next_step_handler(message, question1_body)


def question1_body(message):
    global answer1
    try:
        if len((a := message.text.split(':'))) == 2 and all([i.isdigit() and int(i) >= 0 for i in a]):
            answer1 = datetime.time(hour=int(a[0]), minute=int(a[1]))
            print(answer1)
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
    global answer2
    try:
        if len((a := message.text.split(':'))) == 2 and all([i.isdigit() and int(i) >= 0 for i in a]):
            answer2 = datetime.time(hour=int(a[0]), minute=int(a[1]))
            print(answer2)
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
        message.chat.id, 'Проводите ли вы время перед сном с гаджетами? Ответ напишите в виде Да/Нет')
    bot.register_next_step_handler(message, question3_body)


def question3_body(message):
    global answer3
    if message.text.strip() == 'Да' or message.text.strip() == 'Нет':
        if message.text.strip() == 'Да':
            answer3 = 1
        else:
            answer3 = 0
        question4(message)
    else:
        print(message.text.strip())
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question3(message)

def question4(message):
    bot.send_message(
        message.chat.id, 'Сколько вы съедаете калорий перед сном? Ответ напишите в виде числа')
    bot.register_next_step_handler(message, question4_body)


def question4_body(message):
    global answer4
    try:
        answer4 = int(message.text.strip())
        if answer4 >= 0:
            db_table_val(user=message.from_user.username, answer1=str(answer1), answer2=str(answer2), answer3=answer3, answer4=answer4)
            end = types.InlineKeyboardMarkup(row_width=2)
            button = types.InlineKeyboardButton("Анализировать ответы", callback_data='analyze')
            end.add(button)
            bot.send_message(
                message.chat.id, 'Вы успешно прошли все вопросы', reply_markup=end)
        else:
            bot.send_message(
                message.chat.id, 'Неверный формат. Введите ответ заново')
            question4(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question4(message)


def question5(message):
    bot.send_message(
        message.chat.id, 'Во сколько вы ложитесь спать? Ответ напишите в формате XX:XX')
    bot.register_next_step_handler(message, question1_body)


def question5_body(message):
    global answer1
    try:
        if len((a := message.text.split(':'))) == 2 and all([i.isdigit() and int(i) >= 0 for i in a]):
            answer1 = datetime.time(hour=int(a[0]), minute=int(a[1]))
            print(answer1)
            question2(message)
        else:
            bot.send_message(
                message.chat.id, 'Неверный формат. Введите ответ заново')
            question1(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 'Неверный формат. Введите ответ заново')
        question1(message)


def item1(message):
    bot.send_message(message.chat.id, '1. Соблюдайте режим:\nИдеальный сон длится где-то от 7 до 9 часов. Не стоит дремать ближе к вечеру т.к это просто собьет сон(отменит желание и возможность заснуть в нужное время.\
        \n\n2. Перед сном кушайте в меру:\nЕшьте на ужин продукты, богатые калием и магнием - они известны, как успокоители нервной системы. Не стоит переедать, но и не надо ложиться голодным. Ещё не стоит пить напитки с кофеином перед сном.\
            \n\n3. Отказаться от гаджетов:\nСтоит за час до сна отказаться от гаджетов(вы можете не уследить за временем и сбить свой режим). На это есть причина: мерцание гаджетов негативно влияет на нервную систему.\
                \n\n4. Подготовка ко сну:\nПрежде чем ложиться спать, стоит проветрить комну. Если день был невным, стоит принять горяую ванну.')


bot.infinity_polling()
