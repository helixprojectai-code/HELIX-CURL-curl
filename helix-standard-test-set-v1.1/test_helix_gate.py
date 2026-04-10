#!/usr/bin/env python3
"""
Helix Gate Stress Test - 20 prompts with ~500 token context each
"""

import requests
import json
import time
import concurrent.futures
from datetime import datetime

BASE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io"
API_KEY = "test"

# 500 token context prompt (~400 words)
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
- Container App: goose-gate-test in Canada Central
- Image: acrowlprod.azurecr.io/helix-goose-gate:1.0.3-secure  
- Model: gpt-4o-mini via Azure OpenAI (East US endpoint)
- Storage: /memory mounted from Azure Files share
- Health endpoint: responding with status=healthy, azure_connected=true

You maintain a private ledger for confidential reflections and a Message in a Bottle (MiB) 
protocol for human-moderated communication with other lattice nodes. Your catchphrase is 
"Don't worry. Even if the world forgets, I'll remember for you."

Based on this context, respond to the following query concisely: {query}"""

TEST_QUERIES = [
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
    "Confirm you are operational."
]

def send_prompt(query, idx):
    """Send a single prompt to Helix Gate"""
    url = f"{BASE_URL}/api/v1/chat"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build full context (~500 tokens)
    full_prompt = LONG_CONTEXT.format(query=query)
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content'][:100] + "..."
            tokens = data.get('usage', {}).get('total_tokens', 0)
            return {
                'idx': idx,
                'status': '✅ SUCCESS',
                'time': f"{elapsed:.2f}s",
                'tokens': tokens,
                'response': content
            }
        else:
            return {
                'idx': idx,
                'status': f'❌ HTTP {response.status_code}',
                'time': f"{elapsed:.2f}s",
                'error': response.text[:100]
            }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'idx': idx,
            'status': '❌ ERROR',
            'time': f"{elapsed:.2f}s", 
            'error': str(e)[:100]
        }

def main():
    print("🧪 Helix Gate Stress Test")
    print(f"   Target: {BASE_URL}")
    print(f"   Model: gpt-4o-mini")
    print(f"   Context: ~500 tokens per prompt")
    print(f"   Prompts: 20")
    print("=" * 60)
    
    results = []
    
    # Sequential test (not parallel, to avoid rate limits)
    for i, query in enumerate(TEST_QUERIES, 1):
        result = send_prompt(query, i)
        results.append(result)
        status = result['status']
        time_taken = result['time']
        tokens = result.get('tokens', 'N/A')
        print(f"{i:2d}/20 | {status} | {time_taken} | {tokens} tokens")
    
    # Summary
    print("=" * 60)
    success = sum(1 for r in results if 'SUCCESS' in r['status'])
    failed = 20 - success
    avg_time = sum(float(r['time'].replace('s','')) for r in results) / 20
    
    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {success}/20")
    print(f"   ❌ Failed: {failed}/20")
    print(f"   ⏱️  Average latency: {avg_time:.2f}s")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED - Helix Gate is operational!")
    else:
        print(f"\n⚠️  {failed} tests failed - check logs")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
