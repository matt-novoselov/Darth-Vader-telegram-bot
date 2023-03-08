from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import ChatGPT
import random

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


def Chance(chance):
    return random.random() < chance / 100


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("Приветствую тебя. Я - Дарт Вейдер, повелитель тёмной стороны Силы.")
    with open('Stickers/greet.webp', 'rb') as photo:
        await message.answer_document(photo)


@dp.message_handler(commands='clear')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    ChatGPT.users_prompts[user_id] = []
    ChatGPT.users_prompts[user_id].extend(ChatGPT.template)
    await message.reply("История сообщений была очищена")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    full_response = ChatGPT.ProcessPrompt(message.text, message.from_user.id)
    reaction_index = full_response.rfind('%')
    extracted_text = full_response[:reaction_index]
    extracted_emoji = full_response[reaction_index + 1:]
    await message.answer(extracted_text)
    if Chance(40) and extracted_emoji != 'neutral':
        with open(f'Stickers/{extracted_emoji}.webp', 'rb') as photo:
            await message.answer_document(photo)


if __name__ == '__main__':
    executor.start_polling(dp)
