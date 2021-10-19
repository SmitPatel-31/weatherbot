import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
import requests, json
from datetime import datetime

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "2028143718:AAFguVCqQ0PB4wvGGzpFgEK0_RqzFu43cTQ"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(update,context):
    """callback function for /start handler"""
    bot=context.bot
    author = update.message.from_user.first_name
    reply = "Hi! {} Enter your City name which weather you want to know...".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def _help(update,context):
    bot=context.bot
    """callback function for /help handler"""
    help_txt = "Hey! This is a help text."
    bot.send_message(chat_id=update.message.chat_id, text=help_txt)


def echo_text(update,context):
    """callback function for text message handler"""

    bot=context.bot

    reply = update.message.text

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + reply + "&appid=" + "e3175df7e5869596f69b5c848a2e499d"+"&units=metric"
    response = requests.get(URL)
    latt=0
    lonn=0
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = main['temp']
        temperature_min = main['temp_min']
        temperature_max = main['temp_max']
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather']
        coor= data['coord']
        lat=coor['lat']
        wind  = data['wind']
        w_speed  = wind['speed']
        w_degree = wind['deg']
        lon=coor['lon']
        sys = data['sys']
        country = sys['country']
        sunrise = int(sys['sunrise'])
        sunset = int(sys['sunset'])
        cloud =  data['clouds']
        clouds = cloud['all']


        sunrise1=datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
        sunset1=datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

        # URL2="http://api.openweathermap.org/data/2.5/air_pollution?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=e3175df7e5869596f69b5c848a2e499d"
        # response2 = requests.get(URL2)
        # aqi=None
        # if  response2.status_code == 200:
        #     data1 = response2.json()
        #     list = data1['list']
        #
        #     main= list[1:]
        #     aqi=main['aqi']


        bot.send_message(chat_id=update.message.chat_id, text=f"Country Code:  {country}\n City Name: {reply}\n\n📍 Latitude: {lat} \n📍 Longnitude: {lon}\n\n\n🌡️  Temprature : {temperature} Celsius, \n\n🌡️ Max Temprature : {temperature_max} Celsius\n\n🌡️ Min Temprature : {temperature_min} Celsius\n\n💧Humidity : {humidity} %\n\n↕️ Pressure : {pressure} hPa\n\n☁️ Cloudiness : {clouds} % \n\n️ 🪁 Wind Speed {w_speed} m/s at {w_degree} deg \n\n "
                                                              f"🌅 Sunrise : {sunrise1} \n\n 🌄 Sunset : {sunset1}\n\n" )


    else:
        # showing the error message
        bot.send_message(chat_id=update.message.chat_id,
                         text="Error...")




def error(update,context):
    bot=context.bot
    """callback function for error handler"""
    logger.error("Update '%s' caused error '%s'", update, update.error)


bot = Bot(TOKEN)
try:
    bot.set_webhook("https://weatherbot-by-39-98.herokuapp.com/"+TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(MessageHandler(Filters.text, echo_text))
dp.add_error_handler(error)


if __name__ == "__main__":
    app.run(port=8443)
