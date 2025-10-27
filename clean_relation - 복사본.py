import json
from collections import Counter
import re

# 데이터셋 로드
with open("example_triples.json", "r") as f:
    data = json.load(f)

# Relation 빈도 계산
relations = [item["Relation"] for item in data]
relation_counts = Counter(relations)

# 기호 제거를 위한 함수
def clean_relation(relation):
    # 마침표 등 불필요한 기호를 제거
    return re.sub(r'[^\w\s]', '', relation)

# 빈도가 10 이하인 Relation을 제거하고, 기호를 제거한 데이터셋 생성
cleaned_data = []
for item in data:
    relation = item["Relation"]
    cleaned_relation = clean_relation(relation)
    
    # Relation을 10회 이상 사용한 경우만 포함
    if relation_counts[relation] > 10:
        cleaned_item = item.copy()
        cleaned_item["Relation"] = cleaned_relation
        cleaned_data.append(cleaned_item)

# 정리된 데이터셋 저장
with open("cleaned_triples.json", "w") as f:
    json.dump(cleaned_data, f, indent=4)

print(f"총 {len(cleaned_data)}개의 트리플이 남았습니다.")
