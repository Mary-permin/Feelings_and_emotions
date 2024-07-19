import telebot
from dotenv import load_dotenv, find_dotenv
import os
from g4f.client import Client
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


load_dotenv(find_dotenv())
API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN)

session = {}
# @bot.message_handler(commands=["start"])
# def send_welcome(message):
#     chatID = message.chat.id
#     session[chatID] = {}
#     bot.send_message(chatID, "Для запуска введите команду"
#                              "/find_character")
#

@bot.message_handler(commands=["start"])
def ask(message):
    chatID = message.chat.id
    session[chatID]['message'] = message
    print(chatID)
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Лубой Персонаж🤔", callback_data="character")
    button2 = InlineKeyboardButton("Персонаж Мультфильма🌠🎆", callback_data="disney")
    button3 = InlineKeyboardButton("Персонаж Игры👾🎮", callback_data="game")
    button4 = InlineKeyboardButton("Персонаж Фильма🌇🎥", callback_data="film")
    button5 = InlineKeyboardButton("Персонаж из Сериала🌃🎬", callback_data="serial")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    markup.add(button5)
    bot.send_message(chatID, "Привет, этот бот может помочь тебе найти похожего на себя персонажа\n"
                             "Можешь выбрать категорию, какого именно персонажа🥳👇", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback:True)
def handle_callback1(callback):
    chatID = callback.from_user.id
    button_call = callback.data
    if button_call == "character":
        bot.send_message(chatID, "Опишите себя")
        # bot.register_next_step_handler(session[chatID]['message'], generate_character)
    elif button_call == "disney":
        bot.send_message(chatID, "Опишите себя")
    elif button_call == "game":
        bot.send_message(chatID, "Опишите себя")
    elif button_call == "film":
        bot.send_message(chatID, "Опишите себя")
    elif button_call == "serial":
        bot.send_message(chatID, "Опишите себя")

# @bot.message_handler(commands=["find_character"])
# def ask(message):
#
def generate_character(message):
    chatID = message.chat.id
    bot.send_message(chatID, "Бот ищет подходящего персонажа, подождите пожалуйста")
    bot.send_message(chatID, info_wolfram(message, " на какого персонажа я похож?"))


def info_wolfram(query):
    client = Client()
    response = client.chat.comption.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content


bot.infinity_polling()