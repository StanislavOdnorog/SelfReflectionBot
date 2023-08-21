import os
from dotenv import load_dotenv
import asyncio
from aiogram import Dispatcher, Bot, types
import openai
from aiogram.utils import executor

async def generate_response(prompt):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return chat_completion

load_dotenv(".env")
bot_api_key = os.environ.get("BOT_API_KEY", default=None)
openai.api_key = os.environ.get("OPENAI_API_KEY", default=None)

bot = Bot(bot_api_key)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    with open("./logs/" + str(message.from_user.id), 'a') as f:
        start_message = "Здравствуйте!\n\nЯ здесь чтобы помочь Вам\n\nВся переписка здесь останется строго между нами. Не стесняйтесь в выражениях и проявлении эмоций\n\nВ суете повседневной жизни мы часто упускаем возможность остановиться и подумать о том, что происходит внутри нас. Анализировать свои чувства, разбираться в своих реакциях, а также исследовать свои мотивации — важные шаги на пути к самопознанию и личностному росту\n\nЕсли не знаете с чего начать, то я могу предложить Вам список начальных вопросов:\n1. Какое событие недавно вызвало сильные эмоции? Что вы чувствовали?\n2. Чем Вы гордитесь в своей жизни? Какие чувства это вызывает?\n3. Когда вы в последний раз чувствовали себя неуверенно?\n4. Как вы реагируете на критику? Бывает ли позитивный результат?\n5. Чем любите заниматься в свободное время?\n6. Есть ли люди в вашей жизни, от которых вы зависите?\n7. Как Вы справляетесь с повседневным стрессом?\n8. Какие Ваши главные жизненные ценности? \n9. Какие ваши мечты и цели?"
        await message.reply(start_message)
        f.write("BOT: " + start_message)

@dp.message_handler()
async def respond(message : types.Message):
    with open("./logs/" + str(message.from_user.id), 'a') as f:
        f.write("PERSON: " + message.text + "\n")

    with open("./logs/" + str(message.from_user.id), 'r') as f:
        logs = ""
        for line in (f.readlines()[-10:]):
            logs += line

    with open("./logs/" + str(message.from_user.id), 'a') as f:
        ai_message = await generate_response("Представь что ты психолог. Поддержи человека в любой ситуации, но не отклоняйся от психологии (На все не больше 20-30 слов). Ты мужчина и не надо писать перед каждым сообщением двоеточие. Пиши ответ сразу, не как в логе. Вот лог переписки и последнее сообщение: " + logs)
        f.write("BOT:" + ai_message.choices[0].message.content + "\n")

    await bot.send_message(message.from_user.id, ai_message.choices[0].message.content)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
