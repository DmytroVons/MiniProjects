import logging

import aiohttp
from aiogram import Bot, Dispatcher, types, executor

# Initialize the bot
bot = Bot(token='MY_TEST_TOKEN')
dp = Dispatcher(bot)

# Initialize logging
logging.basicConfig(level=logging.INFO)


# Define a class to manage the bot
class MyTelegramBot:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp

    async def start(self, message: types.Message):
        """
        Handler for the /start command.

        Args:
            message (types.Message): The message from the user.
        """
        await message.answer("Hello! I'm ready to respond to your messages.")

    async def help(self, message: types.Message):
        """
        Handler for the /help command.

        Args:
            message (types.Message): The message from the user.
        """
        help_text = "This is a help message with a list of available commands:\n"
        help_text += "/start - Begin the interaction\n"
        help_text += "/help - The help command"
        await message.answer(help_text)

    async def weather(self, message: types.Message, city: str):
        """
        Handler to fetch and display weather information for a given city.

        Args:
            message (types.Message): The message from the user.
            city (str): The city for which weather information is requested.
        """
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        if data['cod'] == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            await message.answer(f"Weather in {city}: {weather_description}, Temperature: {temperature}°C")
        else:
            await message.answer("Sorry, I couldn't fetch the weather information for that city.")

    async def echo(self, message: types.Message):
        """
        Responds to the user's message with the same message.

        Args:
            message (types.Message): The message from the user.
        """
        await message.answer(message.text)


# Initialize the bot object
my_bot = MyTelegramBot(bot, dp)


# Add command handlers
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await my_bot.start(message)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await my_bot.help(message)


@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    command_args = message.get_args()
    if command_args:
        await my_bot.weather(message, command_args)
    else:
        await message.answer("Please provide a city name along with the /weather command.")


@dp.message_handler()
async def echo(message: types.Message):
    await my_bot.echo(message)


# Run the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
