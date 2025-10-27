import json
import re
from tqdm import tqdm
import openai
import os
import time

# OpenAI API 키 설정
openai.api_key = ''

STATE_FILE = 'additional_tail_state.json'

# 기존 상태 로드 함수
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

# 상태 저장 함수
def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

# GPT-4 API 호출 함수
def generate_text(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
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
        except openai.error.OpenAIError as e:
            print(f"API error: {str(e)}. Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(min(2 ** attempt, 60))  # 최대 대기 시간을 60초로 제한
    print(f"Failed to get response after {max_retries} attempts for prompt: {prompt}")
    return None  # None 반환으로 이후 로직에서 건너뛰도록 함

# 추가할 Additional Tail 생성 함수
def generate_additional_tail(tail):
    prompt = f"{tail}. What are 5 related actions or events that might occur in connection with, before, after, or as a variation of this event? Just answer in a list."
    additional_tails_response = generate_text(prompt)
    if additional_tails_response is None:
        return []
    
    additional_tails = [re.sub(r'^\d+\.\s*', '', item.strip()) for item in additional_tails_response.split('\n') if item.strip()]
    return additional_tails[:5]

# Dynamic Relation 생성 함수
def generate_dynamic_relation(tail, additional_tail):
    prompt = f"What kind of relationship does '{additional_tail}' have with '{tail}'? Just answer in a word."
    dynamic_relation_response = generate_text(prompt)
    return dynamic_relation_response if dynamic_relation_response else "Unknown"

# 기존 JSON 파일 불러오기
with open("example.json", "r") as f:
    data = json.load(f)

state=load_state()


# 기존 데이터 구조에서 복사 및 추가 작업 수행
for category, relations in data.items():
    if category not in state:
        state[category] = {}

    for relation, entries in relations.items():
        if relation not in state[category]:
            state[category][relation] = {"processed_entries": []}

        new_entries = []
        for entry in tqdm(entries, desc=f"Processing {relation} in {category}"):
            head = entry["Head"]
            tail = entry["Tail"]

            # 이미 처리된 head-tail 쌍인지 확인
            if {"Head": head, "Tail": tail} in state[category][relation]["processed_entries"]:
                continue

            # 기존 entry를 복사하여 추가적인 5개 항목 생성
            for _ in range(5):
                additional_tails = generate_additional_tail(tail)
                for additional_tail in additional_tails:
                    dynamic_relation = generate_dynamic_relation(tail, additional_tail)
                    # 기존 Head-Tail 쌍에 대해 새로운 Additional Tail 및 Dynamic Relation 추가
                    new_entry = {
                        "Head": head,
                        "Tail": tail,
                        "Additional Tail": additional_tail,
                        "Dynamic Relation": dynamic_relation
                    }
                    new_entries.append(new_entry)

            # 처리된 entry 기록 및 상태 업데이트
            state[category][relation]["processed_entries"].append({"Head": head, "Tail": tail})
            save_state(state)  # 상태 파일 저장

        # 기존 데이터에 새로운 entries 추가
        entries.extend(new_entries)

# 수정된 데이터를 다시 JSON 파일로 저장
with open("example_updated.json", "w") as f:
    json.dump(data, f, indent=4)

# 최종 완료 후 상태 파일 삭제
if os.path.exists(STATE_FILE):
    os.remove(STATE_FILE)
