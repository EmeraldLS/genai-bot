import os
import telebot
import api_call
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN =  os.environ.get("BOT_TOKEN", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel()

def to_markdown(text):
  text = text.replace('•', ' ')
  return Markdown(textwrap.indent(text," ", predicate=lambda _: True))

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, """
🌟 *Welcome to GeminiAI Bot!* 🤖

I'm here to assist you with your queries and provide insightful responses.

Feel free to send in your prompts or questions, and I'll do my best to help you out! ✨
    """, parse_mode="Markdown")

    
@bot.message_handler(commands=["weather"])
def weather_handler(message):
    bot.reply_to(message, """
🌍 Please input the location for which you want to check the weather.
   
For example:
- Type `Ojo, Lagos` for weather in Ojo, Lagos, Nigeria.
- Type `New York City` for weather in New York City, USA.
- Type `Paris` for weather in Paris, France.
   
Feel free to specify a city, region, or even a country! 🌤️
    """, parse_mode="Markdown")
    bot.register_next_step_handler(message, send_weather)

def send_weather(message):
    weather = api_call.get_weather_details(message.text)
    location = weather["location"]
    current = weather["current"]

    text = f"""
🌍 *Current Weather in {location["name"]} - {location["region"]}, {location["country"]}*

🕒 *Local Time*: {location["localtime"]} ({location["tz_id"]})

🌡️ *Temperature*: {current["temp_c"]}°C ({current["temp_f"]}°F)
- Feels like: {current["feelslike_c"]}°C ({current["feelslike_f"]}°F)
- Wind chill: {current["windchill_c"]}°C ({current["windchill_f"]}°F)

💨 *Wind*: {current["wind_dir"]} at {current["wind_kph"]} kph ({current["wind_mph"]} mph)
- Gusts: {current["gust_kph"]} kph ({current["gust_mph"]} mph)

🌬️ *Wind Direction*: {current["wind_degree"]}° ({current["wind_dir"]})
- Wind Speed: {current["wind_kph"]} kph ({current["wind_mph"]} mph)
    """
    bot.reply_to(message, text, parse_mode="Markdown")
    bot.send_location(message.chat.id, location["lat"], location["lon"])

@bot.message_handler(commands=["motivation", "quote"])
def quote_handler(message):
    quote_data = api_call.get_inspirational_quote()
    markdown_text = f"""
📜 *Quote of the Day*

{quote_data["q"]}

Remember these wise words from *{quote_data['a']}*!
"""
    
    bot.reply_to(message, markdown_text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def general_message(message):
    try:
        bot.send_message(message.chat.id, "Hold on, I'm fetching a response...")
        response =  model.generate_content(message.text)
        bot.reply_to(message, to_markdown(response.text).data.__str__(), parse_mode="Markdown")

    except Exception as err:
        bot.send_message(message.chat.id, f"""
Error occured generating response
                         
error detail: {err}
""", parse_mode="Markdown")
    
    

print("BOT IS RUNNING")
bot.infinity_polling()