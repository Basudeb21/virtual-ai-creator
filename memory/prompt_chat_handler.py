# memory/prompt_chat_handler.py

import json
from pathlib import Path
import subprocess
PROMPTS_FILE = Path("memory/prompts.json")
USER_CHAT_FILE = Path("memory/user_chat.json")

with PROMPTS_FILE.open("r", encoding="utf-8") as f:
    PROMPTS = json.load(f)


def load_user_chats():
    """Load latest user chat memory from disk"""
    if USER_CHAT_FILE.exists():
        with USER_CHAT_FILE.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_user_chats(user_chats):
    """Persist user chat memory to disk"""
    with USER_CHAT_FILE.open("w", encoding="utf-8") as f:
        json.dump(user_chats, f, indent=4)


def get_prompt(creator_id: int) -> str:
    """Retrieve the stored prompt text for a creator by id"""
    return PROMPTS.get(str(creator_id), "")


def chat_with_creator(creator_id: int, user_id: int, user_message: str) -> str:
    """Generate response via Ollama and update user chat memory"""
    prompt_text = get_prompt(creator_id)
    if not prompt_text:
        return "Sorry, creator not found."

    # Always load latest chats from disk
    user_chats = load_user_chats()
    
    # Ensure creator_id exists, then get/create user_id entry
    user_chats.setdefault(str(creator_id), {})
    chat_history = user_chats[str(creator_id)].setdefault(str(user_id), [])
    
    context = "\n".join(chat_history)

    full_prompt = f"{prompt_text}\n\n{context}\nSubscriber: {user_message}\n\nCreator:"

    try:
        result = subprocess.run(
            ["ollama", "run", "dolphin3:latest"],
            input=full_prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=True
        )
        response = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        response = f"Ollama error: {e.stderr.strip()}"

    # Update chat history
    chat_history.append(f"Subscriber: {user_message}")
    chat_history.append(f"Creator: {response}")
    user_chats[str(creator_id)][str(user_id)] = chat_history[-20:]  

    # Save back to disk
    save_user_chats(user_chats)

    return response
