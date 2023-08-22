import os
from dotenv import load_dotenv
import asyncio
from aiogram import Dispatcher, Bot, types
import openai
from aiogram.utils import executor
from aiogram.types import InputFile

async def generate_response(prompt):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return chat_completion.choices[0].message.content

load_dotenv(".env")
bot_api_key = os.environ.get("BOT_API_KEY", default=None)
openai.api_key = os.environ.get("OPENAI_API_KEY", default=None)

bot = Bot(bot_api_key)
dp = Dispatcher(bot)

commands = ['/start', '/delete', '/download', '/specialist']

@dp.message_handler(commands=['delete'])
async def process_delete_command(message: types.Message):
    with open("./logs/" + str(message.from_user.id), 'w') as f:
        f.write(" ")
        await bot.send_message(message.from_user.id, "Все сообщения были успешно удалены из базы!")

@dp.message_handler(commands=['download'])
async def process_download_command(message: types.Message):
    path = "./logs/" + str(message.from_user.id)
    await message.answer_document(InputFile(path))
    await bot.send_message(message.from_user.id, "Лог переписки направлен!")

@dp.message_handler(commands=['specialist'])
async def process_specialist_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Обратись к специалистам сервисов yasno.live, bemeta.co, green-mirt.ru, alter.ru, специалистам других сервисов или по номеру телефона доверия: +78002000122\n\nСкачай переписку с помощью '/download' и дай специалисту с ней ознакомиться")

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    with open("./logs/" + str(message.from_user.id), 'a') as f:
        start_message = "Здравствуйте!\n\nВся переписка здесь останется строго между нами. Не стесняйтесь в выражениях и проявлении эмоций!"
        await bot.send_message(message.from_user.id, start_message)

@dp.message_handler()
async def process_other_messages(message: types.Message):
  
    with open("./logs/" + str(message.from_user.id), 'a') as f:
        if not message.text.startswith('/'):
            f.write(message.text + "\n\n")
        
    with open("./logs/" + str(message.from_user.id), 'r') as f:
        logs = ""
        for line in (f.readlines()[-7:]):
            if not line[0] == '/':
                logs += line
            
    with open("./logs/" + str(message.from_user.id), 'a') as f:
        ai_message = await generate_response("НЕЛЬЗЯ ПИСАТЬ ОТВЕТ БОЛЬШЕ 20 СЛОВ!!! Поддержи человека в любой ситуации не используя формальные термины. Будь как друг, но не отклоняйся от темы помощи (НЕЛЬЗЯ ПИСАТЬ ОТВЕТ БОЛЬШЕ 20-30 СЛОВ!!!). Ты мужчина. Помогай советуй и поддерживай, а не отправляй к специалисту в любой ситуации. Иногда можешь попросить человека продолжить мысль, если не совсем понял его, а иногда задавай вопросы, чтобы раскрыть для человека его проблему. Будь проще, не заставляй человека очень нервничать. (НЕЛЬЗЯ ПИСАТЬ ОТВЕТ БОЛЬШЕ 20 СЛОВ!!!) Вот лог переписки и последнее сообщение, ответь ТОЛЬКО НА ПОСЛЕДНЕЕ СООБЩЕНИЕ: " + logs)
        f.write(ai_message + "\n\n")
        await bot.send_message(message.from_user.id, ai_message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
