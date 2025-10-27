# from openai import OpenAI







# client = OpenAI()
# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "user", "content": "write a haiku about ai"}
#     ]
# )


import openai
import json
from tqdm import tqdm
import re
import os
import time
# OpenAI API 키 설정
openai.api_key = ''


def generate_text(prompt):
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()
        
prompt="hi"

print(generate_text(prompt))