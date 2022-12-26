import telebot
import os

from time import sleep
from flask import Flask, request
from aws.database_service import *

TOKEN = os.environ.get('TELEBOTTOKEN') 
TABLENAME = os.environ.get('RDSTABLENAME')  

bot = telebot.TeleBot(token=TOKEN, threaded=False)
app = Flask(__name__)


@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    
    text = f'Welcome to the WarnerMe-Bot! WarnerMe is here to warn you when your code is compiled! Please type /help for more info.'
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):

    text = f'- When you type \'/id\' you will get a unique id. \n- You can update your requested process by this id.\n- You have to register by using \'/register\' if it is your first time\n- You can check your code status by \'/status\''
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['id']) # help message handler
def send_welcome(message):

    text = f'Your id is {message.from_user.id}. You can use it on Warner-Me Api to change your code status.'
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['register']) # help message handler
def send_welcome(message):

    connection = start_rds_connection()

    if check_record(connection,TABLENAME,message.from_user.id):

        text = f"User {message.from_user.id} already exist in our database."
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    else:

        insert_record(connection,TABLENAME, message.from_user.id, 'deactive', message.chat.id, '')
        text = f'You are registered. You can set your code status by your unique id : {message.from_user.id}'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

        text = f'Your code status is inactive. You can set it active before running your code script.'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    connection.close()

@bot.message_handler(commands=['status']) # help message handler
def send_welcome(message):

    connection = start_rds_connection()
    if check_record(connection,TABLENAME,message.from_user.id) == 0:

        text = f"You are not registered in our database. Please register by /register"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    else:

        record = get_status_record(connection,TABLENAME,message.from_user.id)
        code_status = record['status']
        result = record['result']
        text = f'Your code is {code_status} now. Results: {result}'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    connection.close()

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():

    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():

    #bot.remove_webhook()
    sleep(2)
    bot.set_webhook(url='https://warnerme-bot.onrender.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=int(os.environ.get('PORT')))

