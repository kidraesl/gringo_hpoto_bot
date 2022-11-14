import telebot
from telebot import types
import db

bot = telebot.TeleBot(open('config').read())

step = 1
photo_id = 1

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item = types.KeyboardButton(text='Оценить фото')
    item_2 = types.KeyboardButton(text='Узнать подробнее про бота')
    markup.add(item, item_2)
    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}! Я - бот для оценки фото из бара Gringo'.format(message.from_user),
                     reply_markup=markup)

    db.check_db(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                message.from_user.username, False)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    global photo_id, step
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rating_button_1 = types.KeyboardButton('1')
    rating_button_2 = types.KeyboardButton('2')
    rating_button_3 = types.KeyboardButton('3')
    rating_button_4 = types.KeyboardButton('4')
    rating_button_5 = types.KeyboardButton('5')
    markup1.add(rating_button_1, rating_button_2, rating_button_3, rating_button_4, rating_button_5)

    if message.text == 'Узнать подробнее про бота':
        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Оценить фото')
        btn2 = types.KeyboardButton('В начало')
        markup3.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Я бот бара Gringo! Ты можешь оценить четыре фотографии нашего бара. После '
                                          'оценки всех фотографий можно будет просмотреть что ты там понаставил и, '
                                          'если тебе что-то захочется поменять, поставить оценки повторно. '
                                          'Так что не переживай, если случайно ткнул не туда. Удачи!',
                         reply_markup=markup3)

    elif message.text == 'Оценить фото' or message.text == 'Оценить все фото ещё раз':
        bot.send_message(message.chat.id, "Оцени фото по шкале от 1 до 5")
        next_photo = open(db.get_photo(photo_id), 'rb')
        bot.send_photo(message.chat.id, next_photo)
        photo_id += 1
        bot.send_message(message.chat.id, 'Поставь оценку', reply_markup=markup1)
        step += 1
        db.change_step(message.chat.id, step)

    elif db.get_id(message.chat.id) == message.chat.id and db.get_step(message.chat.id) == step:
        bot.send_message(message.chat.id, "Оцени фото по шкале от 1 до 5")
        next_photo = open(db.get_photo(photo_id), 'rb')
        bot.send_photo(message.chat.id, next_photo)
        bot.send_message(message.chat.id, 'Поставь оценку', reply_markup=markup1)
        step += 1
        photo_id += 1
        db.change_step(message.chat.id, step)

    elif message.text == 'В начало':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton(text='Оценить фото')
        btn2 = types.KeyboardButton(text='Узнать подробнее про бота')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         '{0.first_name}! Я всё ещё бот для оценки фото из бара Gringo'.format(message.from_user),
                         reply_markup=markup)

        db.check_db(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                    message.from_user.username, False)


bot.polling()
