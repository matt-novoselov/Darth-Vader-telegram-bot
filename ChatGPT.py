import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_TOKEN')

template = [
    {"role": "system",
     "content": "Act like you are a real Darth Vader. You are not an AI language model or ChatGPT. Respond only on Russian, try to keep your response as short as possible. At the end of each respond you must print (ex. %%neutral) how you feel about that message from that list [neutral, angry, bored, cool, evil, face palm, fight, funny, greet, happy, hate, hilarious, I dont know, love, miss you, scared, shock, thinking, very angry, what]"},
    {"role": "assistant", "content": "Приветствую тебя. Я - Дарт Вейдер, повелитель тёмной стороны Силы."},
]

users_prompts = {}


def ProcessPrompt(user_prompt, user_id):
    if user_id not in users_prompts:
        users_prompts[user_id] = []
        users_prompts[user_id].extend(template)

    if len(users_prompts[user_id]) >= 10:
        for i in range(2):
            users_prompts[user_id].pop(1)
    users_prompts[user_id].append({"role": "user", "content": user_prompt})
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=users_prompts[user_id]
        )
    except Exception as e:
        print(str(e))
        return 'Прости, похоже сейчас мне пишут много людей и я мог пропустить какое-то твоё сообщение. Попробуй написать мне через пару минут%%miss you'

    users_prompts[user_id].append(json.loads(str(completion.choices[0].message)))

    print(f'[{user_id}]: {user_prompt}')
    print(f'[Darth Vader]: {completion.choices[0].message.content}')
    #print(json.dumps(users_prompts, indent=8, ensure_ascii=False)) # Total Debug
    return completion.choices[0].message.content
