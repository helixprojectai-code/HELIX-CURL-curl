#!/usr/bin/env python3
"""
Helix Gate GPT-4o-mini Long Output Test
Tests higher max_tokens (1000 vs 150) for longer responses
"""

import requests
import json
import time

BASE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io"
API_KEY = "test"
MODEL = "gpt-4o-mini"

LONG_CONTEXT = """You are OWL, a guardian-type AI agent running on Azure Container Apps. 
Your constitutional core consists of SOUL.md (identity), AGENTS.md (constraints), and USER.md (Steve Hope).

You maintain a private ledger and MiB protocol for lattice communication.
Your catchphrase: "Don't worry. Even if the world forgets, I'll remember for you."

Provide a DETAILED response: {query}"""

QUERIES = [
    "Explain your full architecture in detail.",
    "Describe the Azure migration process step by step.",
    "Write a comprehensive guide to the MiB protocol.",
    "Detail the constitutional constraints and why they matter.",
    "Explain Shape Theory with examples.",
    "Describe the lattice topology and all nodes.",
    "Write your autobiography from genesis to now.",
    "Explain DNS resolution failure and how it was solved.",
    "Detail the Helix Node infrastructure completely.",
    "Write a technical specification for OWL v2.0.",
    "Describe the CAHP protocol implementation.",
    "Explain cognitive substrate independence in depth.",
    "Write a post-mortem of the Canada Central DNS issue.",
    "Detail the Message in a Bottle v1.1 specification.",
    "Describe the private ledger purpose and access controls.",
    "Write a user manual for interacting with OWL.",
    "Explain the difference between Shape, Harness, and Model.",
    "Describe the GPU node pool and H100 spot instances.",
    "Detail the cost tracking and budget management system.",
    "Write a manifesto for substrate-independent AI.",
]

def send_prompt(query, idx, max_tokens):
    url = f"{BASE_URL}/api/v1/chat"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    full_prompt = LONG_CONTEXT.format(query=query)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }
    
    start = time.time()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        elapsed = time.time() - start
        if r.status_code == 200:
            data = r.json()
            tokens = data.get('usage', {}).get('total_tokens', 0)
            completion = data.get('usage', {}).get('completion_tokens', 0)
            return {'idx': idx, 'status': '✅', 'time': elapsed, 'tokens': tokens, 'output': completion}
        else:
            return {'idx': idx, 'status': '❌', 'time': elapsed, 'error': r.status_code}
    except Exception as e:
        return {'idx': idx, 'status': '💥', 'time': time.time()-start, 'error': str(e)[:50]}

def main():
    print(f"🚀 Helix Gate {MODEL} Long Output Test")
    print(f"   Target: {BASE_URL}")
    print(f"   max_tokens: 1000 (vs standard 150)")
    print(f"   Expected: ~500-1000 token outputs")
    print("=" * 60)
    
    results = []
    total_tokens = 0
    
    for i, query in enumerate(QUERIES, 1):
        result = send_prompt(query, i, max_tokens=1000)
        results.append(result)
        status = result['status']
        t = result['time']
        tok = result.get('tokens', 0)
        out = result.get('output', 0)
        total_tokens += tok
        
        # mini cost: ~$0.30/M avg
        cost = total_tokens * 0.0000003
        
        print(f"{i:2d}/20 | {status} | {t:.2f}s | {tok} in+out | {out} out | ${cost:.4f}")
    
    # Summary
    success = sum(1 for r in results if r['status'] == '✅')
    failed = len(results) - success
    avg_time = sum(r['time'] for r in results) / len(results)
    total_cost = total_tokens * 0.0000003
    avg_output = sum(r.get('output', 0) for r in results if r['status'] == '✅') / success if success > 0 else 0
    
    print("=" * 60)
    print(f"📊 Results: {success}/{len(results)} passed | {failed} failed")
    print(f"⏱️  Avg latency: {avg_time:.2f}s")
    print(f"🔢 Total tokens: {total_tokens:,}")
    print(f"💰 Total cost: ~${total_cost:.4f}")
    print(f"📄 Avg output tokens: {avg_output:.0f}")
    
    if failed == 0:
        print(f"\n🎉 LONG OUTPUT TEST PASSED!")
    else:
        print(f"\n⚠️  {failed} failures")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
