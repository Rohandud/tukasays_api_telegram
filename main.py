import telebot
import json
import flask
import random
from indic_transliteration import sanscript
import os
from dotenv import load_dotenv, dotenv_values 
app = flask.Flask(__name__)
load_dotenv()
# Load quotes from the JSON file
with open('/home/rohanphulari2/tukasays/tukasays.json', 'r', encoding='utf-8') as file:
    quotes = json.load(file)
url = 'https://rohanphulari2.pythonanywhere.com/'
# Token of your Telegram bot
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
# bot.set_webhook(url=url)

# Initialize the bot
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if flask.request.method == 'POST':
        update = telebot.types.Update.de_json(flask.request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        return 'Hello', 200


@bot.message_handler(commands=['start'])
def start(message):
  user_name = message.from_user.first_name
  print("start "+user_name)
  bot.reply_to(message, "Hey "+user_name +"")
def sanitize_message(message):
    if message.endswith(" ||"):
        return message[:-3]  # Remove the last 3 characters (" ||")
    else:
        return message

# Handler for the /quote command
@bot.message_handler(commands=['quote'])
def send_quote(message):
    # Select a random quote
    random_quote = random.choice(quotes)

    # Split the Marathi quote into lines using the verse number as delimiter
    marathi_lines = random_quote['marathi'].split('॥')

    # Construct the response message
    response = f"{marathi_lines[0].strip()}\n"
    verse_number = 1
    i = 1
    while i < len(marathi_lines):
        if 'ध्रु' in marathi_lines[i]:
            response += f"{marathi_lines[i].strip()}॥\n{marathi_lines[i+1].strip()} ॥"
            i += 2
        else:
            response += f"{marathi_lines[i].strip()}॥\n{marathi_lines[i+1].strip()} ॥"
            i += 2
            verse_number += 1
    english = sanscript.transliterate(response, sanscript.DEVANAGARI, sanscript.ITRANS).lower()
    # Send the response
    response = '📜 Marathi: \n'+response + '📜English :\n'+english
    bot.reply_to(message, sanitize_message(response))

# Start the bot

if __name__ == '__main__':
    app.run(debug=True)
