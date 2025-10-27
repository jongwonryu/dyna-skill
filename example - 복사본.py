import openai
import json
from tqdm import tqdm
import re
import os
import time
# OpenAI API 키 설정
openai.api_key = ''

head_category = {
    "Social-Interaction Relations": [
        "Exercise", "Education", "Work", "Household", "Travel", "Healthcare", "Shopping", 
        "Social Interaction", "Hobbies", "Community Service", "Environmental Conservation", 
        "Technology Use", "Finance", "Entertainment", "Food and Dining", "Personal Development", 
        "Pets and Animals", "Sports", "Arts and Crafts", "Fashion", "Relationship Management", 
        "Cultural Activities", "Legal Matters", "Spirituality", "Home Improvement", 
        "Networking", "Travel and Exploration", "Parenting", "Emergency Response", 
        "Career Development"
    ],
    "Physical-Entity Relations": [
        "Tools", "Appliances", "Vehicles", "Office Supplies", "Medical Equipment", 
        "Kitchen Utensils", "Electronics", "Furniture", "Clothing", "Accessories", 
        "Building Materials", "Food Ingredients", "Clothing Materials", 
        "Electronic Components", "Chemical Compounds", "Art Supplies", "Instruments", 
        "Toys", "Sporting Goods", "Packaging", "Household Items", "Jewelry", 
        "Musical Instruments", "Gardening Tools", "Cleaning Supplies", "Stationery", 
        "Personal Care Products", "Footwear", "Lighting Fixtures", "Outdoor Equipment"
    ],
    "Event-Centered Relations": [
        "Festivals", "Meetings", "Classes", "Sporting Events", "Concerts", "Weddings", 
        "Conferences", "Parties", "Ceremonies", "Projects", "Exams", "Performances", 
        "Trips", "Launch Events", "Meals", "Outdoor Activities", "Travel Plans", 
        "Construction Projects", "Public Gatherings", "Natural Disasters", "Health Issues", 
        "Financial Crises", "Technological Failures", "Social Movements", "Personal Decisions", 
        "Political Actions", "Corporate Strategies", "Educational Pursuits", "Health Interventions", 
        "Cultural Events"
    ],
    "Causal Relations": [
        "Natural Disasters", "Health Conditions", "Economic Events", "Social Behavior", 
        "Technological Failures", "Political Decisions", "Environmental Changes", 
        "Industrial Accidents", "Climate Events", "Psychological States", "Market Trends", 
        "Legal Changes", "Educational Policies", "Cultural Shifts", "Infrastructure Failures", 
        "Agricultural Practices", "Financial Markets", "Public Health Issues", "Resource Depletion", 
        "Human Activities", "Technological Innovations", "Conflict and War", "Population Growth", 
        "Urbanization", "Globalization", "Transportation Incidents", "Cybersecurity Breaches", 
        "Crime Rates", "Workplace Hazards", "Consumer Behavior"
    ],
    "Causal Chain": [
        "Historical Events", "Scientific Discoveries", "Technological Advancements", 
        "Medical Progress", "Industrial Developments", "Business Processes", 
        "Product Development", "Research Projects", "Crisis Management", "Agricultural Cycles", 
        "Supply Chain Logistics", "War and Conflict", "Urban Development", "Space Exploration", 
        "Cultural Evolutions", "Government Policies", "Environmental Conservation", 
        "Innovation Adoption", "Educational Reforms", "Health Care Systems", "Energy Production", 
        "Disaster Response", "Communication Networks", "Military Strategies", "Economic Policies", 
        "Migration Patterns", "Climate Change Adaptation", "Social Movements", 
        "Corporate Strategies", "Public Relations Campaigns"
    ],
    "Temporal Relations": [
        "Daily Routines", "Exercise Activities", "Cooking Tasks", "Work Tasks", 
        "Educational Activities", "Travel Itineraries", "Cleaning Tasks", "Shopping Trips", 
        "Social Events", "Gardening Tasks", "Construction Tasks", "Meeting Agendas", 
        "Leisure Activities", "Sports Activities", "Crafting Projects", "Volunteer Activities", 
        "Medical Procedures", "Beauty Routines", "Study Sessions", "Commutes", "Dining Experiences", 
        "Entertainment Activities", "Family Gatherings", "Fitness Routines", "Home Improvement Tasks", 
        "Technological Setups", "Art Projects", "Financial Planning", "Communication Tasks", 
        "Event Planning"
    ],
    "Duration": [
        "Movies", "Classes", "Meetings", "Sporting Events", "Concerts", "Festivals", "Trips", 
        "Work Shifts", "Medical Appointments", "Training Sessions", "Exams", "Performances", 
        "Workshops", "Cooking Sessions", "Shopping Trips", "Projects", "Games", "Interviews", 
        "Ceremonies", "Lectures", "Repairs", "Appointments", "Discussions", "Competitions", 
        "Conferences", "Tours", "Hikes", "Parties", "Reading Sessions", "Cleaning Tasks"
    ],
    "Frequency": [
        "Exercise", "Grocery Shopping", "Cleaning", "Meetings", "Classes", "Work Tasks", 
        "Social Media Check-ins", "Cooking", "Laundry", "Gardening", "Pet Care", "Medical Check-ups", 
        "Banking", "Car Maintenance", "Reading", "Volunteering", "Traveling", "Family Visits", 
        "Movie Watching", "Sports Practice", "Gaming", "Crafting", "Recycling", "Commuting", 
        "Meditation", "Studying", "Exercise Classes", "Team Meetings", "Hobby Activities", 
        "Shopping for Essentials"
    ],
    "Direction and Movement": [
        "Walking", "Running", "Driving", "Flying", "Cycling", "Swimming", "Sailing", "Hiking", 
        "Skating", "Climbing", "Diving", "Commuting", "Jogging", "Rowing", "Skiing", "Paragliding", 
        "Surfing", "Horse Riding", "Ice Skating", "Rollerblading", "Skateboarding", 
        "Riding a Scooter", "Gliding", "Trekking", "Boating", "Motorcycling", "Hiking", 
        "Mountaineering", "Kayaking", "Driving a Truck"
    ],
    "Conditional Relations": [
        "Weather Conditions", "Health Conditions", "Economic Conditions", "Environmental Conditions", 
        "Social Conditions", "Political Conditions", "Technological Conditions", 
        "Educational Conditions", "Legal Conditions", "Financial Conditions", "Emotional States", 
        "Physical States", "Market Conditions", "Traffic Conditions", "Supply Chain Conditions", 
        "Safety Conditions", "Employment Conditions", "Living Conditions", "Cultural Conditions", 
        "Seasonal Conditions", "Operational Conditions", "Psychological States", "Natural Conditions", 
        "Infrastructure Conditions", "Production Conditions", "Service Conditions", 
        "Compliance Conditions", "Performance Conditions", "Relationship Conditions", 
        "Communication Conditions"
    ],
    "Necessary and Sufficient Conditions": [
        "Medical Procedures", "Legal Actions", "Business Transactions", "Educational Achievements", 
        "Scientific Experiments", "Sports Performances", "Artistic Creations", 
        "Technological Developments", "Construction Projects", "Cooking Recipes", "Travel Plans", 
        "Manufacturing Processes", "Event Planning", "Research Projects", "Financial Investments", 
        "Training Programs", "Negotiations", "Project Management", "Product Development", 
        "Marketing Campaigns", "Crisis Management", "Disaster Response", "Environmental Conservation", 
        "Community Building", "Conflict Resolution", "Policy Implementation", "Software Development", 
        "Agricultural Practices", "Maintenance Tasks", "Quality Control"
    ],
    "Hierarchical Relations": [
        "Animals", "Plants", "Vehicles", "Electronics", "Food and Beverages", "Books", "Movies", 
        "Music Genres", "Sports", "Clothing", "Furniture", "Tools", "Appliances", "Buildings", 
        "Occupations", "Academic Disciplines", "Art Forms", "Software Types", "Languages", "Games", 
        "Materials", "Toys", "Instruments", "Natural Phenomena", "Medical Specialties", 
        "Exercise Types", "Events", "Cosmetics", "Household Items", "Geological Formations"
    ],
    "Part-Whole Relations": [
        "Car", "Computer", "House", "Human Body", "Tree", "Bicycle", "Airplane", "Smartphone", 
        "Book", "Chair", "Guitar", "Watch", "Camera", "Refrigerator", "Television", "Desk", 
        "Ship", "Clock", "Lamp", "Bed", "Building", "Flower", "Animal", "Sandwich", "Machine", 
        "Train", "Painting", "Backpack"
    ],
    "Quantitative Relations" : [
        "Fruits", "Vegetables", "Grains", "Liquids", "Powders", "Solids", "Gases",
        "Tools", "Animals", "Electronic Devides", "Furniture Pieces", "Foods", "Sports Equipment",
        "Plants", "Art Supplies", "Medical Equipment", "Instruments", "Accesories", "Outdoor Equipment",
        "School Supplies", "Jewerly", "Kitchen Utensils", "Chemicals", "Beverages", "Cleaning Products",
        "Vehicles", "Appliances", "Clothing Items", "Building Materials", "Cosmetics"
    ]         
}



relationship_prompts = {
    "Social-Interaction Relations": {
        "xIntent": {
            "Head Prompt": "Name 15 daily actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the possible intention behind this action? Just answer in a word or a sentence."
        },
        "xNeed": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What is needed before performing this action? Just answer in a word or a sentence."
        },
        "xAttr": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What attributes do people who perform this action usually have? Just answer in a word or a sentence."
        },
        "xEffect": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the effect of this action on the person performing it? Just answer in a word or a sentence."
        },
        "xReact": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "How might the person performing this action react? Just answer in a word or a sentence."
        },
        "oEffect": {
            "Head Prompt": "Name 15 actions that affect others related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the effects of this action on others? Just answer in a word or a sentence."
        },
        "oReact": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "How might others react to this action? Just answer in a word or a sentence."
        },
        "oWant": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What might others want to do after witnessing this action? Just answer in a word or a sentence."
        },
        "xWant": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What might the person performing this action want to do next? Just answer in a word or a sentence."
        }
    },
    "Physical-Entity Relations": {
        "ObjectUse": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the typical use of this object? Just answer in a word or a sentence."
        },
        "AtLocation": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "Where is this object typically located? Just answer in a word or a sentence."
        },
        "MadeUpOf": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What material or component make up this object? Just answer in a word or a sentence."
        },
        "HasProperty": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the property of this object? Just answer in a word or a sentence."
        },
        "CapableOf": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What action or function is this object capable of performing? Just answer in a word or a sentence."
        },
        "Desires": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What attribute or condition is desirable for this object? Just answer in a word or a sentence."
        },
        "NotDesires": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What attribute or condition is undesirable for this object? Just answer in a word or a sentence."
        }
    },
    "Event-Centered Relations": {
        "IsAfter": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What usually happens after this event? Just answer in a word or a sentence."
        },
        "HasSubEvent": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the sub-events that occur within this event? Just answer in a word or a sentence."
        },
        "IsBefore": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What usually happens before this event? Just answer in a word or a sentence."
        },
        "HinderedBy": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What factor might hinder or prevent this event from occurring? Just answer in a word or a sentence."
        },
        "Causes": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What causes this event to happen? Just answer in a word or a sentence."
        },
        "xReason": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the reason or motivation behind this event? Just answer in a word or a sentence."
        },
        "isFilledBy": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "What entitie or participant is involved in this event? Just answer in a word or a sentence."
        }
    },
    "Causal Relations": {
        "Cause and Effect": {
            "Head Prompt": "Name 15 causes related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the effect or outcome of this cause? Just answer in a word or a sentence."
        },
        "Causal Chain": {
            "Head Prompt": "Name 15 sequences of events related to {item}. Just answer in a list.",
            "Tail Prompt": "Describe the cause-and-effect relationships that link these events together. Just answer in a word or a sentence."
        }
    },
    "Temporal Relations": {
        "Temporal Sequence": {
            "Head Prompt": "Name 15 activities related to {item}. Just answer in a list.",
            "Tail Prompt": "What typically happens before and after this activity? Just answer in a word or a sentence."
        }
    },
    "Duration":{
        "Duration": {
            "Head Prompt": "Name 15 events related to {item}. Just answer in a list.",
            "Tail Prompt": "How long does this event usually last? Just answer in a word or a sentence."
        }
    },
    "Frequency":{
        "Frequency": {
            "Head Prompt": "Name 15 activities related to {item}. Just answer in a list.",
            "Tail Prompt": "How frequently does this activity occur? Just answer in a word or a sentence."
        }
    },
    "Direction and Movement": {
        "Direction and Movement": {
            "Head Prompt": "Name 15 movements related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the direction of this movement? Just answer in a word or a sentence."
        }
    },
    "Conditional Relations": {
        "If-Then Statements": {
            "Head Prompt": "Name 15 conditions related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the outcome or consequence if this condition is met? Just answer in a word or a sentence."
        }
    },
    "Necessary and Sufficient Conditions": {
        "Necessary and Sufficient Conditions": {
            "Head Prompt": "Name 15 actions related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the necessary and sufficient condition for this action to occur? Just answer in a word or a sentence."
        }
    },
    "Hierarchical Relations": {
        "Category and Subcategory": {
            "Head Prompt": "Name 15 categories related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the subcategorie within this category? Just answer in a word or a sentence."
        }
    },
    "Part-Whole Relations" : {
        "Part-Whole Relations": {
            "Head Prompt": "Name 15 objects related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the part of this object? Just answer in a word or a sentence."
        }
    },
    "Quantitative Relations": {
        "Quantities and Measures": {
            "Head Prompt": "Name 15 items related to {item}. Just answer in a list.",
            "Tail Prompt": "What is the typical quantitie or measurement of this item? Just answer in a word or a sentence."
        },
        "Comparative Relations": {
            "Head Prompt": "Name 15 items related to {item}. Just answer in a list.",
            "Tail Prompt": "How does this item compare to others in terms of size, quantity, or other attributes? Just answer in a word or a sentence."
        }
    }
}


# head_category = {"Social-Interaction Relations": [
#         "Exercise"]}

# relationship_prompts = {
#     "Social-Interaction Relations": {
#         "xIntent": {
#             "Head Prompt": "Name 15 daily actions related to {item}. Just answer in a list.",
#             "Tail Prompt": "What are one possible intention behind this action? Just answer in a word or a sentence."
#         }
#     }
# }


    
STATE_FILE = 'state.json'

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

# def generate_text(prompt, max_retries=5):
#     for attempt in range(max_retries):
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-4-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=500,
#                 n=1,
#                 stop=None,
#                 temperature=0.7
#             )
#             return response.choices[0].message['content'].strip()
#         except openai.error.OpenAIError as e:
#             error_message = str(e)
#             if "The model produced invalid content" in error_message:
#                 print(f"Error: {error_message}. Saving state and exiting.")
#                 return "The model produced invalid content"
#             print(f"API error: {error_message}. Retrying ({attempt + 1}/{max_retries})...")
#             time.sleep(2 ** attempt)  # 지수 백오프
#     print(f"Failed to get response after {max_retries} attempts.")
#     return None


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




# def generate_head_and_tail(prompts, head_category, state):
#     heads_and_tails = state.get('heads_and_tails', {})

#     for category, items in tqdm(head_category.items(), desc="Processing Categories"):
#         for item in tqdm(items, desc=f"Processing Items in {category}", leave=False):
#             for relation, prompt_pair in prompts[category].items():
#                 if category not in heads_and_tails:
#                     heads_and_tails[category] = {}
#                 if relation not in heads_and_tails[category]:
#                     heads_and_tails[category][relation] = []

#                 head_prompt = prompt_pair["Head Prompt"].format(item=item)
#                 tail_prompt = prompt_pair["Tail Prompt"]

#                 if 'current_item' in state and state['current_item'] == item and 'heads_response' in state:
#                     heads_response = state['heads_response']
#                 else:
#                     heads_response = generate_text(head_prompt)
#                     if heads_response == "ERROR: The model produced invalid content":
#                         state['heads_and_tails'] = heads_and_tails
#                         save_state(state)
#                         return heads_and_tails
#                     if heads_response is None:
#                         continue
#                     state['current_item'] = item
#                     state['heads_response'] = heads_response
#                     save_state(state)

#                 heads = [head.strip() for head in heads_response.split('\n') if head.strip()]

#                 for head in tqdm(heads, desc=f"Processing Heads for {item} in {category}", leave=False):
#                     head = re.sub(r'^\d+\.\s*', '', head)
#                     full_tail_prompt = f"{head}. {tail_prompt}"

#                     if 'current_head' in state and state['current_head'] == head and 'tail_response' in state:
#                         tail = state['tail_response']
#                     else:
#                         tail = generate_text(full_tail_prompt)
#                         if tail == "ERROR: The model produced invalid content":
#                             state['heads_and_tails'] = heads_and_tails
#                             save_state(state)
#                             return heads_and_tails
#                         if tail is None:
#                             continue
#                         state['current_head'] = head
#                         state['tail_response'] = tail
#                         save_state(state)

#                     heads_and_tails[category][relation].append({"Head": head, "Tail": tail})

#                     state['heads_and_tails'] = heads_and_tails
#                     save_state(state)

#     return heads_and_tails


def generate_head_and_tail(prompts, head_category, state):
    heads_and_tails = state.get('heads_and_tails', {})

    for category, items in tqdm(head_category.items(), desc="Processing Categories"):
        for item in tqdm(items, desc=f"Processing Items in {category}", leave=False):
            for relation, prompt_pair in prompts[category].items():
                if category not in heads_and_tails:
                    heads_and_tails[category] = {}
                if relation not in heads_and_tails[category]:
                    heads_and_tails[category][relation] = []

                head_prompt = prompt_pair["Head Prompt"].format(item=item)
                tail_prompt = prompt_pair["Tail Prompt"]

                heads_response = generate_text(head_prompt)
                if heads_response is None:
                    print(f"Skipping due to failure in generating heads for item: {item}, category: {category}")
                    continue

                heads = [head.strip() for head in heads_response.split('\n') if head.strip()]

                for head in tqdm(heads, desc=f"Processing Heads for {item} in {category}", leave=False):
                    head = re.sub(r'^\d+\.\s*', '', head)
                    full_tail_prompt = f"{head}. {tail_prompt}"

                    tail = generate_text(full_tail_prompt)
                    if tail is None:
                        print(f"Skipping due to failure in generating tail for head: {head}")
                        continue

                    heads_and_tails[category][relation].append({"Head": head, "Tail": tail})

                    # 중간 상태 저장
                    state['heads_and_tails'] = heads_and_tails
                    save_state(state)

    return heads_and_tails



def generate_additional_tail(tail, state):
    additional_tail_prompt = f"{tail}. What 10 actions are related or similar to this event? Just answer in a list."

    if 'current_tail' in state and state['current_tail'] == tail and 'additional_tails_response' in state:
        additional_tails_response = state['additional_tails_response']
    else:
        additional_tails_response = generate_text(additional_tail_prompt)
        if additional_tails_response == "ERROR: The model produced invalid content":
            state['current_tail'] = tail
            save_state(state)
            return []
        if additional_tails_response is None:
            return []
        state['current_tail'] = tail
        state['additional_tails_response'] = additional_tails_response
        save_state(state)

    additional_tails = [re.sub(r'^\d+\.\s*', '', tail.strip()) for tail in additional_tails_response.split('\n') if tail.strip()]
    return additional_tails[:10]

def generate_dynamic_relation(tail, additional_tail, state):
    dynamic_relation_prompt = f"What kind of relationship does '{additional_tail}' have with '{tail}'? Just answer in a word."

    if 'current_dynamic_tail' in state and state['current_dynamic_tail'] == additional_tail:
        return state['dynamic_relation_response']
                
    dynamic_relation_response = generate_text(dynamic_relation_prompt)
    if dynamic_relation_response == "ERROR: The model produced invalid content":
        state['current_dynamic_tail'] = additional_tail
        save_state(state)
        return None

    state['current_dynamic_tail'] = additional_tail
    state['dynamic_relation_response'] = dynamic_relation_response
    save_state(state)

    return dynamic_relation_response

state = load_state()

results = state.get('results', {})
for category, relations in relationship_prompts.items():
    print(f"Processing Category: {category}")
    results[category] = results.get(category, {})
    heads_and_tails = generate_head_and_tail({category: relations}, {category: head_category[category]}, state)
    for relation, data_list in tqdm(heads_and_tails[category].items(), desc=f"Processing Relations for {category}", leave=False):
        for data in tqdm(data_list, desc=f"Processing Data for {relation} in {category}", leave=False):
            head = data["Head"]
            tail = data["Tail"]

            additional_tails = generate_additional_tail(tail, state)
            if not additional_tails:
                continue
            for additional_tail in tqdm(additional_tails, desc=f"Generating Relations for {tail} in {category}", leave=False):
                dynamic_relation = generate_dynamic_relation(tail, additional_tail, state)
                if dynamic_relation is None:
                    continue

                if relation not in results[category]:
                    results[category][relation] = []
                results[category][relation].append({
                    "Head": head,
                    "Tail": tail,
                    "Additional Tail": additional_tail,
                    "Dynamic Relation": dynamic_relation
                })

                state['results'] = results
                save_state(state)

# 최종 결과 저장
with open('example.json', 'w') as f:
    json.dump(results, f, indent=4)

# 상태 파일 삭제 (작업 완료 후)
if os.path.exists(STATE_FILE):
    os.remove(STATE_FILE)