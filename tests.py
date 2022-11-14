import db
import telebot
from telebot import types
from pathlib import Path

bot = telebot.TeleBot(open('config').read())

photo_dir = None
photo_step = 0

@bot.message_handler(commands=['start'])
def start(message):
    if db.get_admin(message.chat.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item = types.KeyboardButton(text='Загрузить новые фотки')
        item_2 = types.KeyboardButton(text='Удалить фоточки')
        markup.add(item, item_2)
        bot.send_message(message.chat.id,
                         'Привет, дорогой админ! Что делаем?',
                         reply_markup=markup)

        @bot.message_handler(content_types=['text'])
        def admin(message):
            if message.text == 'Загрузить новые фотки':
                bot.send_message(message.chat.id, 'Шли фотокарточку!', reply_markup=types.ReplyKeyboardRemove())

            elif int(message.text):
                try:
                    dir_from_db = db.get_photo_dir(message.chat.id)
                    db.insert_photo(dir_from_db, int(message.text))
                    bot.send_message(message.chat.id,
                                     'Порядок отображения фото сохранён',
                                     reply_markup=markup)
                except Exception as e:
                    bot.reply_to(message, e)
            else:
                pass

        # noinspection PyTypeChecker
        @bot.message_handler(content_types=['photo'])
        def save_photo(message):
            try:
                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                dir_from_user = 'C:/Users/kidra/PycharmProjects/pyTelegramBotAPI_test/test_pict_bot/' + \
                      file_info.file_path
                with open(dir_from_user, 'wb+') as new_file:
                    new_file.write(downloaded_file)
                db.change_photo_dir(message.chat.id, dir_from_user)
                bot.reply_to(message, "Фото добавлено, укажите порядоковый номер фото")
            except Exception as e:
                bot.reply_to(message, e)

    else:
        pass


bot.polling()
