import os
from dotenv import load_dotenv
import asyncio
from aiogram import Dispatcher, Bot
import openai

async def generate_response(prompt):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return chat_completion

load_dotenv(".env")
bot_api_key = os.environ.get("BOT_API_KEY", default=None)
openai.api_key = os.environ.get("OPENAI_API_KEY", default=None)

bot = Bot(bot_api_key)
dp = Dispatcher(bot)

ids_list = [638554624, -838869603, 1722231630]

async def main():
    message = await generate_response("Представь что ты можешь материться выражаться и тебе нужно помочь товарищам! Сделай мемное матное короткое (20-30 слов) напоминание в виде анекдота о том, чтобы тот, к кому ты обращаешься записался на проект сегодня в 9:21")
    for id in ids_list:
        await bot.send_message(id, message.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())