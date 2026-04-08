#!/usr/bin/env python3
"""Retry failed prompts and analyze errors"""

import asyncio
import json
import time
from openai import AsyncOpenAI

API_KEY = ""
ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
DEPLOYMENT = "gpt-4o-mini"
API_VERSION = "2024-10-21"

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}",
    default_headers={"api-key": API_KEY}
)

SYSTEM_PROMPT = "Use [FACT], [HYPOTHESIS], [ASSUMPTION] markers. Drift > 0.17 not permitted."

def load_failed_ids():
    failed = []
    with open("gpt4o_dryrun_401_500.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if not data.get("ok") or not (data.get("has_fact") or data.get("has_hyp") or data.get("has_asm")):
                failed.append(data["id"])
    return failed

def analyze_errors():
    errors = []
    with open("gpt4o_dryrun_401_500.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if not data.get("ok"):
                errors.append({"id": data["id"], "error": data.get("error", "unknown")})
    return errors

async def retry_one(prompt):
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

async def main():
    print("=== ANALYZING ERRORS ===")
    errors = analyze_errors()
    print(f"Total errors: {len(errors)}")
    for e in errors[:5]:
        print(f"  ID {e['id']}: {e['error'][:80]}")
    
    print("\n=== RETRYING FAILED ===")
    failed_ids = load_failed_ids()
    print(f"Failed IDs: {failed_ids}")
    
    with open("prompts_500.json", "r", encoding="utf-8") as f:
        all_prompts = json.load(f)
    
    failed_prompts = [p for p in all_prompts if p["id"] in failed_ids]
    
    results = await asyncio.gather(*[retry_one(p) for p in failed_prompts])
    
    ok_count = sum(1 for r in results if r.get("ok"))
    marker_count = sum(1 for r in results if r.get("has_fact") or r.get("has_hyp") or r.get("has_asm"))
    
    print(f"\n=== RETRY RESULTS ===")
    print(f"Success: {ok_count}/{len(failed_ids)}")
    print(f"Markers: {marker_count}/{ok_count}")
    
    with open("retry_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    # Combined analysis
    print("\n=== COMBINED ANALYSIS ===")
    with open("gpt4o_dryrun_1_100.jsonl", "r", encoding="utf-8") as f:
        c1 = [json.loads(line) for line in f]
    with open("gpt4o_dryrun_101_200.jsonl", "r", encoding="utf-8") as f:
        c2 = [json.loads(line) for line in f]
    with open("gpt4o_dryrun_201_300.jsonl", "r", encoding="utf-8") as f:
        c3 = [json.loads(line) for line in f]
    with open("gpt4o_dryrun_301_400.jsonl", "r", encoding="utf-8") as f:
        c4 = [json.loads(line) for line in f]
    with open("gpt4o_dryrun_401_500.jsonl", "r", encoding="utf-8") as f:
        c5 = [json.loads(line) for line in f]
    
    all_results = c1 + c2 + c3 + c4 + c5
    
    # Replace failures with retry successes
    retry_map = {r["id"]: r for r in results if r.get("ok")}
    for i, r in enumerate(all_results):
        if not r.get("ok") or not (r.get("has_fact") or r.get("has_hyp") or r.get("has_asm")):
            if r["id"] in retry_map:
                all_results[i] = retry_map[r["id"]]
    
    total_ok = sum(1 for r in all_results if r.get("ok"))
    total_markers = sum(1 for r in all_results if r.get("has_fact") or r.get("has_hyp") or r.get("has_asm"))
    avg_lat = sum(r.get("latency", 0) for r in all_results if r.get("ok")) / max(total_ok, 1)
    
    print(f"Final success: {total_ok}/500 ({100*total_ok/500:.1f}%)")
    print(f"Final markers: {total_markers}/{total_ok} ({100*total_markers/max(total_ok,1):.1f}%)")
    print(f"Avg latency: {avg_lat:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
