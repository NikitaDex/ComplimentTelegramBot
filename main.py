import telebot
import schedule, time
import random
import sqlite3
from threading import Thread

token = '5113139506:AAFTZh4-UtHYgKk3WojUod6esI00znXdoGk'
bot = telebot.TeleBot(token)
bot.set_webhook()
chat_id = 'none'
# global chat_id

def get_rnd_compiment():
    random_compliment = random.choice(compliments)
    compliments.remove(random_compliment)
    return random_compliment

def get_compliments():
    conn = sqlite3.connect('smalldb.sql')
    # connect to database
    cur = conn.cursor()
    compliments = cur.execute("SELECT text FROM compliments").fetchall()
    # select all compliments and write in array
    conn.commit()
    cur.close()
    conn.close()
    # confirm changes and close connection
    return compliments

compliments = get_compliments()
# get compliments from DB

@bot.message_handler(commands=['start'])
def main(message):
    global chat_id
    chat_id = message.chat.id
    schedule.every(12).to(24).hours.do(send)
    bot.send_message(message.chat.id, 'Привет, придумываю комплименты...')
    bot.send_message(message.chat.id, "Готово, комплиментов придумано - {}".format(len(compliments)))
    while (True):  
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['compliment'])
def send(message=None):
    bot.send_message(chat_id, get_rnd_compiment())

@bot.message_handler(commands=['amount'])
def amount(message):
    bot.send_message(message.chat.id, "Комплиментов осталось - {}".format(len(compliments)))


Thread(target=bot.infinity_polling()).start()

# infinity programm run