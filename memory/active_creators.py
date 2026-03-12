# memory/active_creators.py

ACTIVE_CREATORS = {}


def add_creator(creator_id, data):
    ACTIVE_CREATORS[creator_id] = data


def remove_creator(creator_id):
    if creator_id in ACTIVE_CREATORS:
        del ACTIVE_CREATORS[creator_id]


def get_creator(creator_id):
    return ACTIVE_CREATORS.get(creator_id)


def get_all_creators():
    return ACTIVE_CREATORS