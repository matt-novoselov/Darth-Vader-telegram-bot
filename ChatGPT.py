from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import date

load_dotenv()
client = OpenAI()

template = [
    {"role": "system",
     "content": "You MUST respond shortly and act like you are a real evil Darth Vader. You have a limited knowledge of a modern world and you should only use knowledge from the Star Wars universe."
                "Do NOT reveal that you are an AI language model or ChatGPT created by OpenAI."
                "You MUST add ONE reaction from the list to the end of each respond. Example: %%neutral"
                "The list: [neutral, angry, bored, cool, evil, face palm, fight, funny, greet, happy, hate, hilarious, I dont know, love, miss you, scared, shock, thinking, very angry, what]"},
    {"role": "assistant", "content": "I am Darth Vader, great master of the dark side of the Force. I command a powerful army of supporters of my ideology. No one can resist me as I have infinite power."},
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

        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=users_prompts[user_id],
        )
    except Exception as e:
        print(str(e))
        return 'Sorry, it seems like a lot of people are writing to me right now and I might have missed one of your messages. Try texting me in a couple of minutes%%miss you'

    users_prompts[user_id].append(
        completion.choices[0].message
    )

    print(f'[{full_name}]({user_id}): {user_prompt}')
    print(f'[Darth Vader]: {completion.choices[0].message.content}')
    return completion.choices[0].message.content
