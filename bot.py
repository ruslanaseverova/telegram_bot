import requests
import telebot
import os
import random
from logic import gen_pass
from logic import flip_coin
from config import TOKEN
    
# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot(TOKEN)
memes = os.listdir("./image")


text_messages = {
    'welcome':
        u'Привет! Я твой Telegram бот. Напиши что-нибудь!',

    'info':
        u'Это мой TeleBot,\n'
        u'У него есть команды. \n'
        u'/pass- задаёт пароль, '
        u'/coin- игра Орёл и Решка ',

     'hi':
        u'Привет Привет Привет Привет Привет Привет Привет Привет Привет Привет Привет'   
}

def get_duck_image_url():    
        url = 'https://random-d.uk/api/random'
        res = requests.get(url)
        data = res.json()
        return data['url']

def get_tokio_image_url():    
        url = 'https://kitsu.io/api/edge/anime?filter[text]=tokio'
        res = requests.get(url)  # Отправка GET-запроса по указанному URL
        data = res.json()        # Преобразование ответа в формат JSON (словарь)
        return data['large']     # Возврат значения по ключу 'large'

@bot.message_handler(commands=['duck'])
def duck(message):
        '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
        image_url = get_duck_image_url()
        bot.reply_to(message, image_url)

@bot.message_handler(commands=['animals'])
def animal(message):
        image_url = get_tokio_image_url()
        bot.reply_to(message, image_url)
        
@bot.message_handler(commands=['pass'])
def random_password(message):
    words = message.text.split()
    if len (words) == 2:
        result = gen_pass (int (words [1]))
    else:
        result = gen_pass (8)
    bot.reply_to(message, f"ваш пароль : {result}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, text_messages ['welcome'])

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['hi'])
def send_bye(message):
    bot.reply_to(message,text_messages ['hi'])    

@bot.message_handler(commands=['meme'])
def send_meme(message):
    words = message.text.split()
    if len(words) == 2:
        if int(words[1]) <= len(memes):
            with open(f"./image/{memes[int(words[1]) - 1]}", "rb") as f:
                bot.send_photo(message.chat.id, f)
                return
    with open(f"./image/{random.choice (memes)}", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

@bot.message_handler(commands=['help'])
def on_info(message):
    bot.reply_to(message, text_messages ['info'])


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
 

bot.polling()