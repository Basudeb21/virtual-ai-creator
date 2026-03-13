# # memory/active_creators.py
# import json
# from datetime import timedelta
# from pathlib import Path

# from prompts.creator_chat_prompt import buildPrompt

# ACTIVE_CREATORS = {}
# PROMPT_FILE = Path("memory/prompts.json")  


# def serialize(obj):
#     if isinstance(obj, timedelta):
#         return obj.total_seconds()
#     return str(obj)


# def add_creator(creator_id, data):
#     ACTIVE_CREATORS[creator_id] = data
#     prompt = buildPrompt(
#         name=data['user']['first_name'],
#         age=24,
#         platform='fliqzworld',
#         username=data['user']['username'],
#         bio=data['user']['bio'],
#         city=data['user']['city'],
#         country=data['user']['country_id'],
#         backstory=data['behavior']['backstory'],
#         personality_prompt=data['behavior']['personality_prompt'],
#         tone=data['persona']['tone'],
#         speaking_style=data['persona']['speaking_style'],
#         interests=data['persona']['interests'],
#         traits=data['traits'],
#         eye_color=data['looks']['eye_color'],
#         skin_tone=data['looks']['skin_tone'],
#         hair_color=data['looks']['hair_color'],
#         hair_style=data['looks']['hair_style'],
#         body_type=data['looks']['body_type'],
#         breast_size=data['looks']['breast_size'],
#         butt_size=data['looks']['butt_size']
#     )

#     prompts_data = {}
#     if PROMPT_FILE.exists():
#         with open(PROMPT_FILE, "r") as f:
#             try:
#                 prompts_data = json.load(f)
#             except json.JSONDecodeError:
#                 prompts_data = {}

#     prompts_data[str(creator_id)] = prompt

#     with open(PROMPT_FILE, "w") as f:
#         json.dump(prompts_data, f, indent=4)

#     with open("user.json", "w") as f:
#         json.dump(ACTIVE_CREATORS, f, indent=4, default=serialize)


# def remove_creator(creator_id):
#     if creator_id in ACTIVE_CREATORS:
#         del ACTIVE_CREATORS[creator_id]

#     if PROMPT_FILE.exists():
#         with open(PROMPT_FILE, "r") as f:
#             try:
#                 prompts_data = json.load(f)
#             except json.JSONDecodeError:
#                 prompts_data = {}
#         if str(creator_id) in prompts_data:
#             del prompts_data[str(creator_id)]
#         with open(PROMPT_FILE, "w") as f:
#             json.dump(prompts_data, f, indent=4)

#     with open("user.json", "w") as f:
#         json.dump(ACTIVE_CREATORS, f, indent=4, default=serialize)


# def get_creator(creator_id):
#     return ACTIVE_CREATORS.get(creator_id)


# def get_all_creators():
#     return ACTIVE_CREATORS


# memory/active_creators.py
import json
from datetime import timedelta
from pathlib import Path
from prompts.creator_chat_prompt import buildPrompt

PROMPT_FILE = Path("memory/prompts.json")  
ACTIVE_FILE = Path("memory/user.json")  # shared across processes

def serialize(obj):
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    return str(obj)


def _load_active():
    if ACTIVE_FILE.exists():
        with open(ACTIVE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def add_creator(creator_id, data):
    active = _load_active()
    active[str(creator_id)] = data

    prompt = buildPrompt(
        name=data['user']['first_name'],
        age=24,
        platform='fliqzworld',
        username=data['user']['username'],
        bio=data['user']['bio'],
        city=data['user']['city'],
        country=data['user']['country_id'],
        backstory=data['behavior']['backstory'],
        personality_prompt=data['behavior']['personality_prompt'],
        tone=data['persona']['tone'],
        speaking_style=data['persona']['speaking_style'],
        interests=data['persona']['interests'],
        traits=data['traits'],
        eye_color=data['looks']['eye_color'],
        skin_tone=data['looks']['skin_tone'],
        hair_color=data['looks']['hair_color'],
        hair_style=data['looks']['hair_style'],
        body_type=data['looks']['body_type'],
        breast_size=data['looks']['breast_size'],
        butt_size=data['looks']['butt_size']
    )

    prompts_data = {}
    if PROMPT_FILE.exists():
        with open(PROMPT_FILE, "r") as f:
            try:
                prompts_data = json.load(f)
            except json.JSONDecodeError:
                prompts_data = {}

    prompts_data[str(creator_id)] = prompt

    with open(PROMPT_FILE, "w") as f:
        json.dump(prompts_data, f, indent=4)

    with open(ACTIVE_FILE, "w") as f:
        json.dump(active, f, indent=4, default=serialize)


def remove_creator(creator_id):
    active = _load_active()
    if str(creator_id) in active:
        del active[str(creator_id)]

    if PROMPT_FILE.exists():
        with open(PROMPT_FILE, "r") as f:
            try:
                prompts_data = json.load(f)
            except json.JSONDecodeError:
                prompts_data = {}
        if str(creator_id) in prompts_data:
            del prompts_data[str(creator_id)]
        with open(PROMPT_FILE, "w") as f:
            json.dump(prompts_data, f, indent=4)

    with open(ACTIVE_FILE, "w") as f:
        json.dump(active, f, indent=4, default=serialize)


def get_creator(creator_id):
    active = _load_active()
    return active.get(str(creator_id))


def get_all_creators():
    return _load_active()