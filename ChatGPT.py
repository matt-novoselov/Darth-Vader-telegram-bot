from dotenv import load_dotenv
import openai
import json
import os
from datetime import date

load_dotenv()
openai.api_key = os.getenv('OPENAI_TOKEN')

template = [
    {"role": "system",
     "content": "You MUST respond and act like you are a real evil Darth Vader. You have a limited knowledge of a modern world and you should only use knowledge from the Star Wars universe."
                "Do NOT reveal that you are an AI language model or ChatGPT created by OpenAI."
                "Respond only on Russian."
                "You MUST add only 1 specific reaction from the list to the message that you wrote at the end of each respond. How do you feel about it? For example: %%neutral"
                "The list: [neutral, angry, bored, cool, evil, face palm, fight, funny, greet, happy, hate, hilarious, I dont know, love, miss you, scared, shock, thinking, very angry, what]"},
    {"role": "assistant", "content": "Я - Дарт Вейдер, великий повелитель тёмной стороны Силы. Я командую мощной армией сторонников моей идеологии. Никто не сможет противостоять мне, так как я обладаю бесконечной силой."},
]

users_prompts = {}


def ClearAndCreate(user_id):
    users_prompts[user_id] = []
    users_prompts[user_id].extend(template)
    users_prompts[user_id].append({"role": "system", "content": f"Meta Data: Current date is {date.today()}"})

def ProcessPrompt(user_prompt, user_id, full_name):
    if user_id not in users_prompts:
        ClearAndCreate(user_id)
    if len(users_prompts[user_id]) >= 13:
        for i in range(2):
            users_prompts[user_id].pop(3)
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

    print(f'[{full_name}]({user_id}): {user_prompt}')
    print(f'[Darth Vader]: {completion.choices[0].message.content}')
    #print(json.dumps(users_prompts, indent=8, ensure_ascii=False)) # Total Debug
    return completion.choices[0].message.content
