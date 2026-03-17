# workers/memory_processor_worker.py
import asyncio
import subprocess
import json
import re

from prompts.memory_processor_prompt import memory_processor_prompt
from queues.queue_manager import pop_processing
from services.keyword_loader import load_keywords
from queues.queue_manager import push_final


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


KEYWORDS = load_keywords()


def process_memory_llm(message: str):
    prompt = memory_processor_prompt(message, KEYWORDS)

    try:
        result = subprocess.run(
            ["ollama", "run", "dolphin3:latest"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=20,
            check=True
        )

        output = result.stdout.strip()

        print("LLM Raw Output:", output)

        json_text = extract_json(output)
        if not json_text:
            print("❌ No JSON found")
            return None

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            print("❌ JSON parse failed")
            return None

        # ✅ FIX 1: validate tag
        tag = data.get("tag", "preference_general")
        if tag not in set(KEYWORDS):
            print("⚠️ Invalid tag from LLM:", tag)
            tag = "preference_general"

        data["tag"] = tag

        return data

    except Exception as e:
        print("LLM Error:", e)
        return None


async def run_worker():
    print("Memory Processor Worker started")

    while True:
        job = pop_processing()

        if not job:
            await asyncio.sleep(2)
            continue

        message = job["message"]

        print("\nProcessing memory:", message)

        result = process_memory_llm(message)

        if not result:
            print("❌ Failed to process memory")
            continue

        # ✅ FIX 2: spelling corrected
        job["summarise_chat"] = result.get("summary", "")
        job["tag"] = result.get("tag", "preference_general")
        job["importance_score"] = result.get("importance_score", 1)

        push_final(job)

        print("✅ Stored in final queue:", job)
        # 👉 NEXT STEP: store in DB


if __name__ == "__main__":
    asyncio.run(run_worker())