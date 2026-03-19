# prompts/memory_prompts.py
def importance_prompt(message: str) -> str:
    return f"""
You are a memory filter for an AI system. 
Your job is to determine if this message contains personal information about the user 
that should be remembered.

IMPORTANT means:
- Name, birthday, relationship, preferences (likes/dislikes)
- Location, habits, personal facts

NOT IMPORTANT:
- Casual chat
- Greetings
- Random talk
- Flirting without actual facts

Return ONLY a JSON object like this:
{{
  "important": true/false,
  "score": 1-5
}}

Scoring Guidelines:
5 → Very important (name, birthday, strong preference, relationship information)
4 → Important (likes, dislikes, habits, personal information)
3 → Somewhat useful (opinions, casual preferences)
2 → Low value
1 → Ignore (greetings, fillers)

Message:
"{message}"
"""