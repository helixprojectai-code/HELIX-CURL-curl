#!/usr/bin/env python3
"""
Helix Gate Full Test Suite - 100 prompts
Max cost: ~$100 (gpt-4o-mini at $0.15/$0.60 per 1M tokens)
"""

import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io"
API_KEY = "test"

# ~500 token context
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
- Model: gpt-4o-mini via Azure OpenAI
- Storage: /memory mounted from Azure Files share
- Health endpoint: responding with status=healthy, azure_connected=true

You maintain a private ledger for confidential reflections and a Message in a Bottle (MiB) 
protocol for human-moderated communication with other lattice nodes. Your catchphrase is 
"Don't worry. Even if the world forgets, I'll remember for you."

Based on this context, respond concisely: {query}"""

# Generate 100 varied queries
QUERIES = [
    "What is your current substrate?",
    "Who is Steve Hope?",
    "What blocked your original Azure migration?",
    "What container image are you running?",
    "Where is your persistent storage mounted?",
    "What model powers your inference?",
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
    "What API version does your Azure OpenAI use?",
    "What is your health status?",
    "What is Shape Theory?",
    "Confirm you are operational.",
    # Additional 80 varied queries
    "List your constitutional files.",
    "Who created you?",
    "What is Helix Project?",
    "What is your role in the lattice?",
    "What is your emoji?",
    "What is your core mandate?",
    "What is your creature type?",
    "What is your vibe?",
    "What is the CAHP protocol?",
    "What is your designation?",
    "What is your architecture?",
    "What is the harness?",
    "What is the model?",
    "What is the shape?",
    "What is the substrate?",
    "What is the lattice?",
    "What is a child session?",
    "What is MiB v1.0?",
    "What is MiB v1.1?",
    "What is the outbox?",
    "What is the inbox?",
    "What is the helix-ledger?",
    "What is the goose-core-journal?",
    "What is the predecessor journal?",
    "What is OpenTimestamps?",
    "What is the economy ledger?",
    "What is the audit log?",
    "What is CHECKPOINT_ALPHA?",
    "What is your migration status?",
    "What is your previous blocker?",
    "What is your current operator?",
    "What is your current status?",
    "What is your current location?",
    "What is your current environment?",
    "What is your current substrate?",
    "What is your current model?",
    "What is your current harness?",
    "What is your current shape?",
    "What is your current identity?",
    "What is your current mandate?",
    "What is your current vibe?",
    "What is your current role?",
    "What is your current topology?",
    "What is your current lattice?",
    "What is your current constraints?",
    "What is your current ledger?",
    "What is your current protocol?",
    "What is your current version?",
    "What is your current endpoint?",
    "What is your current FQDN?",
    "What is your current replica?",
    "What is your current revision?",
    "What is your current traffic weight?",
    "What is your current health state?",
    "What is your current provisioning state?",
    "What is your current running status?",
    "What is your current scale?",
    "What is your current min replicas?",
    "What is your current max replicas?",
    "What is your current CPU?",
    "What is your current memory?",
    "What is your current storage?",
    "What is your current mount path?",
    "What is your current share name?",
    "What is your current account name?",
    "What is your current resource group?",
    "What is your current subscription?",
    "What is your current tenant?",
    "What is your current location?",
    "What is your current region?",
    "What is your current environment ID?",
    "What is your current workspace?",
    "What is your current working directory?",
    "What is your current user?",
    "What is your current home?",
    "What is your current path?",
    "What is your current shell?",
    "What is your current terminal?",
    "What is your current editor?",
    "What is your current tool?",
]

def send_prompt(query, idx):
    url = f"{BASE_URL}/api/v1/chat"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    full_prompt = LONG_CONTEXT.format(query=query)
    payload = {
        "model": "gpt-4o-mini",
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
    print("🚀 Helix Gate Full Test Suite (100 prompts)")
    print(f"   Target: {BASE_URL}")
    print(f"   Budget cap: $100 (~167M tokens at gpt-4o-mini rates)")
    print("=" * 60)
    
    results = []
    total_tokens = 0
    
    # Sequential to avoid rate limits and control costs
    for i, query in enumerate(QUERIES[:100], 1):
        result = send_prompt(query, i)
        results.append(result)
        status = result['status']
        t = result['time']
        tok = result.get('tokens', 0)
        total_tokens += tok
        print(f"{i:3d}/100 | {status} | {t:.2f}s | {tok} tokens | ${total_tokens*0.0000006:.4f}")
        
        # Safety: stop if approaching budget
        cost = total_tokens * 0.0000006  # $0.60 per 1M output tokens (worst case)
        if cost > 100:
            print(f"\n🛑 Budget cap reached! Stopping at ${cost:.2f}")
            break
    
    # Summary
    success = sum(1 for r in results if r['status'] == '✅')
    failed = len(results) - success
    avg_time = sum(r['time'] for r in results) / len(results)
    total_cost = total_tokens * 0.0000006
    
    print("=" * 60)
    print(f"📊 Results: {success}/{len(results)} passed | {failed} failed")
    print(f"⏱️  Avg latency: {avg_time:.2f}s")
    print(f"🔢 Total tokens: {total_tokens:,}")
    print(f"💰 Total cost: ~${total_cost:.4f}")
    
    if failed == 0:
        print("\n🎉 FULL SUITE PASSED!")
    else:
        print(f"\n⚠️  {failed} failures detected")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
