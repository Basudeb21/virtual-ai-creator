# prompts/memory_processor_prompt.py
def memory_processor_prompt(message: str, keywords: list[str]) -> str:
    keyword_list = ", ".join(keywords)

    return f"""
You are an AI memory processor.

Your job is to extract structured memory from a user message.

Message:
"{message}"

Available tags (STRICT):
[{keyword_list}]

Instructions:
- Choose ONLY ONE tag from the available tags
- DO NOT create new tags
- If nothing fits, use: preference_general

Extract:

1. summary (max 15 words)
2. tag (must be from list)
3. importance_score (1 to 10)

Return ONLY valid JSON:

{{
  "summary": "...",
  "tag": "...",
  "importance_score": 0
}}
"""