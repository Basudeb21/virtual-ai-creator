# workers/importance_worker.py
import asyncio
import subprocess
from prompts.memory_prompts import importance_prompt
from queues.queue_manager import pop_msg, push_processing
import json

def check_importance_llm(message: str) -> bool:
    prompt = importance_prompt(message)

    try:
        result = subprocess.run(
            ["ollama", "run", "dolphin3:latest"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30,
            check=True
        )

        output = result.stdout.strip()
        print("LLM Raw Output:", output)

        data = json.loads(output)
        score = data.get("score", 0)
        important = data.get("important", False)

        return important or score >= 3

    except Exception as e:
        print("LLM Error:", e)
        return False
async def run_worker():
    print("Importance worker started")

    while True:
        job = pop_msg()
        print('JOB :: ', job)

        if not job:
            await asyncio.sleep(2)
            continue

        message = job["message"]

        print("\nChecking importance:", message)

        is_important = check_importance_llm(message)

        if is_important:
            push_processing(job)
            print("✅ Important → moved to processing queue")
        else:
            print("❌ Not important → skipped")


if __name__ == "__main__":
    asyncio.run(run_worker())