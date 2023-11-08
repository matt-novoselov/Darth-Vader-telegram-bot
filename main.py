import asyncio
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import ChatGPT
import random
import whisper

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


def Chance(chance):
    return random.random() < chance / 100


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("Hello, I am a Darth Vader, great master of the dark side of the Force."
                        "\n\nSend me a text or voice message - I will reply"
                        "\n\nUse /clear to clear message history")
    with open('Stickers/greet.webp', 'rb') as photo:
        await message.answer_document(photo)


@dp.message_handler(commands='clear')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    ChatGPT.ClearAndCreate(user_id)
    await message.reply("Message history was cleared")


async def MakeRequest(message, text_message):
    full_name = message.from_user.full_name
    loop = asyncio.get_event_loop()
    full_response = await loop.run_in_executor(None, ChatGPT.ProcessPrompt, text_message, message.from_user.id,
                                               full_name)
    reaction_index = full_response.rfind('%%')
    extracted_text = full_response[:reaction_index]
    extracted_emoji = full_response[reaction_index + 2:]
    await message.reply(extracted_text)
    if extracted_emoji != 'neutral':
        if Chance(70):  # %
            try:
                with open(f'Stickers/{extracted_emoji}.webp', 'rb') as photo:
                    await message.answer_document(photo)
            except:
                print("[!] Error. I was unable to open and send sticker")
                pass


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    await MakeRequest(message,message.text)


@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_message_handler(message: types.Message):
    voice = await message.voice.get_file()
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path

    await bot.download_file(file_path, destination=f"Temp/{voice.file_id}.ogg")
    transcribed_text = await whisper.Transcribe(voice.file_id)
    if transcribed_text:
        print(f"[v] Voice message transcribed successfully: {transcribed_text}")
        await MakeRequest(message, transcribed_text)
    os.remove(f"Temp/{voice.file_id}.ogg")
    os.remove(f"Temp/{voice.file_id}.wav")


if __name__ == '__main__':
    executor.start_polling(dp)
