import os
from dotenv import load_dotenv
import asyncio
from aiogram import Dispatcher, Bot, types
import openai
from aiogram.utils import executor
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext

load_dotenv(".env")
bot_api_key = os.environ.get("BOT_API_KEY", default=None)
openai.api_key = os.environ.get("OPENAI_API_KEY", default=None)

bot = Bot(bot_api_key)
dp = Dispatcher(bot)

async def generate_response(prompt):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return chat_completion

# Create a state for command processing
class CommandProcessingState(StatesGroup):
    processing = State()  # This state represents that a command is being processed

@dp.message_handler(Command(['delete', 'download', 'specialist', 'start']))
async def process_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data.processing = True  # Set the processing flag

    if message.text.startswith('/delete'):
        with open("./logs/" + str(message.from_user.id), 'w') as f:
            f.write(" ")
            await bot.send_message(message.from_user.id, "Все сообщения были успешно удалены из базы!")
        pass
    elif message.text.startswith('/download'):
        with open("./logs/" + str(message.from_user.id), 'rb') as f:
            path = "./logs/" + str(message.from_user.id)
            await message.answer_document(InputFile(path))
            await bot.send_message(message.from_user.id, "Лог переписки направлен!")
        pass
    elif message.text.startswith('/specialist'):
        await bot.send_message(message.from_user.id, "Обратись к специалистам сервисов yasno.live, bemeta.co, green-mirt.ru, alter.ru, специалистам других сервисов или по номеру телефона доверия: 88002000122\n\nСкачай переписку с помощью '/download' и дай специалисту с ней ознакомиться")
        pass
    elif message.text.startswith('/start'):
        with open("./logs/" + str(message.from_user.id), 'a') as f:
            start_message = "Здравствуйте!\n\nВся переписка здесь останется строго между нами. Не стесняйтесь в выражениях и проявлении эмоций!"
            await bot.send_message(message.from_user.id, start_message)
        pass

    async with state.proxy() as data:
        data.processing = False  # Reset the processing flag

@dp.message_handler(lambda message: not message.text.startswith('/'))
async def process_other_messages(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not data.processing:
            with open("./logs/" + str(message.from_user.id), 'a') as f:
                f.write(message.text + "\n\n")
            with open("./logs/" + str(message.from_user.id), 'r') as f:
                logs = ""
                for line in (f.readlines()[-15:]):
                    logs += line
            with open("./logs/" + str(message.from_user.id), 'a') as f:
                ai_message = await generate_response("НЕЛЬЗЯ ПИСАТЬ ОТВЕТ БОЛЬШЕ 20-30 СЛОВ!!! Поддержи человека в любой ситуации не используя формальные термины. Будь как друг, но не отклоняйся от темы помощи (НЕЛЬЗЯ ПИСАТЬ ОТВЕТ БОЛЬШЕ 20-30 СЛОВ!!!). Ты мужчина. Помогай советуй и поддерживай, а не отправляй к специалисту в любой ситуации. Иногда можешь попросить человека продолжить мысль, если не совсем понял его. Будь проще, не заставляй человека очень нервничать. (НЕЛЬЗЯ ПИСАТЬ ОТВЕТ БОЛЬШЕ 20-30 СЛОВ!!!) Вот лог переписки и последнее сообщение, ответь ТОЛЬКО НА ПОСЛЕДНЕЕ СООБЩЕНИЕ: " + logs)
                f.write(ai_message.choices[0].message.content + "\n\n")    
            await bot.send_message(message.from_user.id, ai_message.choices[0].message.content)
            pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
