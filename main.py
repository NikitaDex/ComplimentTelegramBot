import telebot
import time
import random
import sqlite3

token = '511139506:AAFZh4-UtHYgK3WoUod6esI00znXdo'
# telegram bot token (not real)
bot = telebot.TeleBot(token)

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

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет, придумываю комплименты...')
    compliments = get_compliments()
    # get array
    bot.send_message(message.chat.id, "Готово, комплиментов придумано - {}".format(len(compliments)))
    while (True):  
        bot.send_message(message.chat.id, compliments.pop())
        # take last item in array and del it
        time.sleep(random.randint(86400,129600))
        # bot sleep 1 ... 1,5 day

bot.polling(none_stop=True)
# infinity programm run