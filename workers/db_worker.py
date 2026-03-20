# workers/db_worker.py
import asyncio
from queues.queue_manager import pop_final
from database.ai_creator_queries import insert_memory
from database.db import db  # your existing DB module

async def run_worker():
    print("DB Worker started")

    while True:
        job = pop_final()
        print('Final JOB ', job)

        if not job:
            await asyncio.sleep(2)
            continue

        try:
            
            # ✅ Insert memory using the proper keyword
            insert_memory(
                ai_id=job.get("ai_id"),
                fan_id=job.get("fan_id"),
                keyword=job.get("keyword"),
                summary=job.get("summarise_chat", ""),
                importance_score=job.get("importance_score", 1)
            )

            print(f"✅ Stored in DB: AI {job.get('ai_id')} Fan {job.get('fan_id')} Keyword {'keyword'}")

        except Exception as e:
            print("❌ Memory insert failed:::", e)
            await asyncio.sleep(1)  # prevent rapid crash loop


if __name__ == "__main__":
    asyncio.run(run_worker())