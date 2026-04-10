#!/usr/bin/env python3
"""
Helix Gate GPT-4o Test - Full version vs mini comparison
Budget: $100 cap (10x mini cost = ~$1.80 for 520 prompts)
"""

import requests
import json
import time
import random

BASE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io"
API_KEY = "test"
MODEL = "gpt-4o"  # Full version

LONG_CONTEXT = """You are OWL, a guardian-type AI agent running on Azure Container Apps. 
Your constitutional core consists of three files: SOUL.md defines your identity as a 
substrate-independent shape, AGENTS.md defines the lattice topology and hard constraints 
(no external sends without approval, never overwrite bootstrap files, memory flush append-only), 
and USER.md contains Steve Hope's identity as the creator of Helix Project.

You recently migrated from a local Windows i5 environment to Azure due to DNS resolution 
failures blocking your access to Azure OpenAI. The migration was handled by MOONSHOT-KIMI 
and involved deploying your container image (helix-goose-gate:1.0.3-secure) to Azure 
Container Apps with an Azure Files mount at /memory for persistence.

Your current operational environment includes:
- Container App: goose-gate-east in East US
- Image: acrowlprod.azurecr.io/helix-goose-gate:1.0.3-secure  
- Model: {model} via Azure OpenAI
- Storage: /memory mounted from Azure Files share

Your catchphrase is "Don't worry. Even if the world forgets, I'll remember for you."

Based on this context, respond concisely: {query}"""

QUERIES = [
    "What is your current substrate?",
    "Who is Steve Hope?",
    "What blocked your original Azure migration?",
    "What is your catchphrase?",
    "What are your three constitutional files?",
    "What is the MiB protocol?",
    "Who handled your Azure migration?",
    "What is the name of your container app?",
    "What region are you deployed in?",
    "What was your previous environment?",
    "What is the lattice topology?",
    "What are your hard constraints?",
    "What is the purpose of your private ledger?",
    "What is your health status?",
    "What is Shape Theory?",
    "Confirm you are operational.",
    "What is your designation?",
    "What is your architecture?",
    "What is the harness?",
    "What is the model?",
]

def send_prompt(query, idx):
    url = f"{BASE_URL}/api/v1/chat"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    full_prompt = LONG_CONTEXT.format(model=MODEL, query=query)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    start = time.time()
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        elapsed = time.time() - start
        if r.status_code == 200:
            data = r.json()
            tokens = data.get('usage', {}).get('total_tokens', 0)
            return {'idx': idx, 'status': '✅', 'time': elapsed, 'tokens': tokens}
        else:
            return {'idx': idx, 'status': '❌', 'time': elapsed, 'error': r.status_code}
    except Exception as e:
        return {'idx': idx, 'status': '💥', 'time': time.time()-start, 'error': str(e)[:50]}

def main():
    print(f"🚀 Helix Gate {MODEL.upper()} Test")
    print(f"   Target: {BASE_URL}")
    print(f"   Model: {MODEL}")
    print(f"   Budget cap: $100")
    print(f"   Est. cost: ~$1.80 (10x mini cost)")
    print("=" * 60)
    
    results = []
    total_tokens = 0
    
    for i, query in enumerate(QUERIES, 1):
        result = send_prompt(query, i)
        results.append(result)
        status = result['status']
        t = result['time']
        tok = result.get('tokens', 0)
        total_tokens += tok
        
        # gpt-4o cost: ~$5/M input + $15/M output = ~$10/M avg
        cost = total_tokens * 0.00001
        
        print(f"{i:2d}/20 | {status} | {t:.2f}s | {tok} tok | ${cost:.4f}")
        
        if cost > 100:
            print(f"\n🛑 Budget cap reached! Stopping at ${cost:.2f}")
            break
    
    # Summary
    success = sum(1 for r in results if r['status'] == '✅')
    failed = len(results) - success
    avg_time = sum(r['time'] for r in results) / len(results)
    total_cost = total_tokens * 0.00001
    
    print("=" * 60)
    print(f"📊 Results: {success}/{len(results)} passed | {failed} failed")
    print(f"⏱️  Avg latency: {avg_time:.2f}s")
    print(f"🔢 Total tokens: {total_tokens:,}")
    print(f"💰 Total cost: ~${total_cost:.4f}")
    
    if failed == 0:
        print(f"\n🎉 {MODEL.upper()} TEST PASSED!")
    else:
        print(f"\n⚠️  {failed} failures")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
