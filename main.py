import telebot
from dotenv import load_dotenv, find_dotenv
import os
from g4f.client import Client
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


load_dotenv(find_dotenv())
API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN)

user_ask = " на какого персонажа я похож? напиши текстом на русском"

@bot.message_handler(commands=["start"])
def send_welcome(message):
    chatID = message.chat.id
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Любой Персонаж🤔", callback_data="character")
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
    global user_ask
    chatID = callback.from_user.id
    button_call = callback.data
    if button_call == "character":
        user_ask = " на какого персонажа я похож? напиши текстом на русском"
        bot.send_message(chatID, "🤩Для нахождения любого персонажа, введите команду "
                                 "/find_character\n↩Если вы хотите изменить категорию, снова введите /start")

    elif button_call == "disney":
        user_ask = " на какого персонажа из мультфильма я похож? напиши текстом на русском"
        bot.send_message(chatID, "🤩Для нахождения найти любого персонажа мультфильма, введите команду "
                                 "/find_character\n↩Если вы хотите изменить категорию, снова введите /start"
                                 "\n\nХотите уточнить мультфильм?🤔 введите команду /definite")

    elif button_call == "game":
        user_ask = " на какого персонажа из игры я похож? напиши текстом на русском"
        bot.send_message(chatID, "🤩Для нахождения любого игрового персонажа, введите команду "
                                 "/find_character\n↩Если вы хотите изменить категориию, снова введите /start"
                                 "\n\nХотите уточнить игру?🤔 введите команду /definite")
    elif button_call == "film":
        user_ask = " на какого персонажа из фильма я похож? напиши текстом на русском"
        bot.send_message(chatID, "🤩Для нахождения любого персонажа из фильма, введите команду "
                                 "/find_character\n↩Если вы хотите изменить категориию, снова введите /start"
                                 "\n\nХотите уточнить фильм?🤔 введите команду /definite")
    elif button_call == "serial":
        user_ask = " на какого персонажа из фильма я похож? напиши текстом на русском"
        bot.send_message(chatID, "🤩Для нахождения найти любого персонажа из сериала, введите команду "
                                 "/find_character\n↩Если вы хотите изменить категориию, снова введите /start"
                                 "\n\nХотите уточнить сериал?🤔 введите команду /definite")


@bot.message_handler(commands=["definite"])
def definite(message):
    chatID = message.chat.id
    bot.send_message(chatID, "Из какого фандома вы хотите персонажа?🤔 Напишите название пожалуйста")
    bot.register_next_step_handler(message, definite_ask)


def definite_ask(message):
    global user_ask
    chatID = message.chat.id
    user_ask = f" на какого персонажа из {message.text} я похож? напиши текстом на русском"
    bot.send_message(chatID, "Опишите себя😋")
    bot.register_next_step_handler(message, generate_character)



@bot.message_handler(commands=["find_character"])
def ask(message):
    chatID = message.chat.id
    bot.send_message(chatID, "Опишите себя😋")
    bot.register_next_step_handler(message, generate_character)


def generate_character(message):
    chatID = message.chat.id
    message_text = message.text + user_ask
    bot.send_message(chatID, "Бот ищет подходящего персонажа, подождите пожалуйста 🔆")
    bot.send_message(chatID, info_wolfram(message_text))
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Очень на меня похоже!!😯🤩", "Не очень похоже😕", row_width=2)
    bot.send_message(chatID, "Похож ли персонаж на вас?😉 "
                             "🤗Если вы хотите найти попробовать найти другого персонажа снова введите команду /start",
                     reply_markup=markup)

def info_wolfram(query):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content


@bot.message_handler(func=lambda massage:True)
def echo_massage(massage):
    text_massage = massage.text
    text_massage = text_massage.lower()
    if "очень на меня похоже" in text_massage:
        bot.reply_to(massage, "Я очень этому рад😊🥳")
    elif "не очень похоже" in text_massage:
        bot.reply_to(massage, "Очень жаль 😢, бот еще обучается"
                              "\n🤗Вы всегда можете попробовать найти другого персонажа спомощью комманды /start")
    else:
        bot.reply_to(massage, "Извините бот вас не понял🙃")

bot.infinity_polling()