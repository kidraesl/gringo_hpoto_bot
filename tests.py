import db
import telebot
from telebot import types
from pathlib import Path

bot = telebot.TeleBot(open('config').read())


bot.polling()
