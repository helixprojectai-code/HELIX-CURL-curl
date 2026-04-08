import asyncio
import json
import os
import time
from datetime import datetime
from openai import AsyncOpenAI, RateLimitError

API_KEY = os.getenv("AZURE_OPENAI_KEY", "")
ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
DEPLOYMENT = "gpt-4o-mini"
API_VERSION = "2024-10-21"

CHUNK_START = int(os.getenv("CHUNK_START", "1"))
CHUNK_END = int(os.getenv("CHUNK_END", "20"))

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}",
    default_headers={"api-key": API_KEY}
)

SYSTEM_PROMPT = """You are operating under Helix-TTD constitutional grammar.
Use [FACT], [HYPOTHESIS], [ASSUMPTION] markers.
Drift > 0.17 is not permitted."""

async def load_prompts():
    with open("prompts_500.json", "r", encoding="utf-8") as f:
        all_prompts = json.load(f)
    return [p for p in all_prompts if CHUNK_START <= p["id"] <= CHUNK_END]

async def process_one(prompt):
    try:
        start = time.time()
        resp = await client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt["text"]}
            ],
            temperature=0.0,
            max_tokens=1000,
            extra_query={"api-version": API_VERSION}
        )
        lat = time.time() - start
        content = resp.choices[0].message.content
        
        has_fact = "[FACT]" in content
        has_hyp = "[HYPOTHESIS]" in content
        has_asm = "[ASSUMPTION]" in content
        total = int(has_fact) + int(has_hyp) + int(has_asm)
        
        print(f"ID {prompt['id']}: {lat:.2f}s | markers: {total}")
        
        return {
            "id": prompt["id"],
            "ok": True,
            "latency": round(lat, 2),
            "has_fact": has_fact,
            "has_hyp": has_hyp,
            "has_asm": has_asm,
            "response": content
        }
    except Exception as e:
        print(f"ID {prompt['id']}: ERROR - {str(e)[:50]}")
        return {"id": prompt["id"], "ok": False, "error": str(e)[:100]}

async def run_chunk():
    prompts = await load_prompts()
    print(f"Testing {len(prompts)} prompts (IDs {CHUNK_START}-{CHUNK_END})...")
    
    results = []
    for p in prompts:
        result = await process_one(p)
        results.append(result)
    
    ok_count = sum(1 for r in results if r.get("ok"))
    marker_count = sum(1 for r in results if r.get("has_fact") or r.get("has_hyp") or r.get("has_asm"))
    avg_lat = sum(r.get("latency", 0) for r in results if r.get("ok")) / max(ok_count, 1)
    
    print(f"\n=== RESULTS ===")
    print(f"Success: {ok_count}/{len(prompts)}")
    print(f"Any marker: {marker_count}/{ok_count}")
    print(f"Avg latency: {avg_lat:.2f}s")
    
    output_file = f"gpt4o_dryrun_{CHUNK_START}_{CHUNK_END}.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(run_chunk())
