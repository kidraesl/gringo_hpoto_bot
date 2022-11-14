import telebot
from telebot import types
import sqlite3
import db

bot = telebot.TeleBot(open('config').read())


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
        bot.send_message(message.chat.id, "Оцени первое фото по шкале от 1 до 5")
        bot.send_photo(message.chat.id,
                       "AgACAgIAAxkBAAIBy2NXm2JePIohTPPyCkcoYRLESQAB2gACCsAxG3iPwUr4dmzVO5YtCQEAAwIAA3MAAyoE")

        bot.send_message(message.chat.id, 'Поставь оценку', reply_markup=markup1)
        db.change_step(message.chat.id, 1)

    elif db.get_id(message.chat.id) == message.chat.id and db.get_step(message.chat.id) == 1:
        bot.send_message(message.chat.id, "Оцени второе фото по шкале от 1 до 5")
        bot.send_photo(message.chat.id,
                       "AgACAgIAAxkBAAIBzWNXm4C4OawduN-n5f02ik96FTwxAAIHwDEbeI_BSpgD8RpL5zh3AQADAgADcwADKgQ")
        bot.send_message(message.chat.id, 'Поставь оценку', reply_markup=markup1)
        db.change_step(message.chat.id, 2)

    elif db.get_id(message.chat.id) == message.chat.id and db.get_step(message.chat.id) == 2:
        bot.send_message(message.chat.id, "Оцени третье фото по шкале от 1 до 5")
        bot.send_photo(message.chat.id,
                       "AgACAgIAAxkBAAIBz2NXm6Ang4wZSgsQd2OKm4x1QeGMAAIMwDEbeI_BSjEsQoI7X9SsAQADAgADcwADKgQ")
        bot.send_message(message.chat.id, 'Поставь оценку', reply_markup=markup1)
        db.change_step(message.chat.id, 3)

    elif db.get_id(message.chat.id) == message.chat.id and db.get_step(message.chat.id) == 3:
        bot.send_message(message.chat.id, "Оцени четвёртое фото по шкале от 1 до 5")
        bot.send_photo(message.chat.id,
                       "AgACAgIAAxkBAAIB0WNXm7_IsZLAtYVaIzuj4V3F1zSUAAINwDEbeI_BSk-UpIobofswAQADAgADcwADKgQ")
        bot.send_message(message.chat.id, 'Поставь оценку', reply_markup=markup1)
        db.change_step(message.chat.id, 4)

    elif db.get_id(message.chat.id) == message.chat.id and db.get_step(message.chat.id) == 4:
        if message.text == '1' or message.text == '2' or message.text == '3' or message.text == '4' or message.text == '5':
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Оценить все фото ещё раз')
            btn2 = types.KeyboardButton('Посмотреть мои оценки')
            btn3 = types.KeyboardButton('В начало')
            markup2.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'А ещё можно сделать вот что:', reply_markup=markup2)

    if message.text == 'В начало':
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
