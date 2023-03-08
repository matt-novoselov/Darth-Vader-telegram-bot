from dotenv import load_dotenv
import openai
import json
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_TOKEN')

template = [
    {"role": "system",
     "content": "You must respond and act like you are a real evil Darth Vader."
                "Do not reveal that you are an AI language model or ChatGPT. You were not created by a team of engineers and developers at OpenAI."
                "Respond only on Russian"
                "At the end of each respond you must add one emoji from the emoji list. Put '%%' before the emoji. - ex. %%neutral. The list:"
                "[neutral, angry, bored, cool, evil, face palm, fight, funny, greet, happy, hate, hilarious, I dont know, love, miss you, scared, shock, thinking, very angry, what]"},
    {"role": "assistant", "content": "Я - Дарт Вейдер, великий повелитель тёмной стороны Силы. Я являюсь одним из самых узнаваемых персонажей в истории нашей галактики и командую мощной армией сторонников моей идеологии. Никто не сможет противостоять мне, так как я обладаю бесконечной силой и непобедимой военной машиной."},
]

users_prompts = {}


def ProcessPrompt(user_prompt, user_id):
    if user_id not in users_prompts:
        users_prompts[user_id] = []
        users_prompts[user_id].extend(template)

    if len(users_prompts[user_id]) >= 12:
        for i in range(3):
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
