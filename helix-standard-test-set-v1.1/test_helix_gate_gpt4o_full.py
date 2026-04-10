#!/usr/bin/env python3
"""
Helix Gate GPT-4o Full Test - 520 prompts
Budget: ~$10-15 (well under $100 cap)
"""

import requests
import json
import time
import random

BASE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io"
API_KEY = "test"
MODEL = "gpt-4o"

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

QUERY_TEMPLATES = [
    "What is {topic}?",
    "Explain {topic} briefly.",
    "Define {topic}.",
    "Describe {topic}.",
    "How does {topic} work?",
    "Why is {topic} important?",
]

TOPICS = [
    "your substrate", "the lattice", "the shape", "the harness", "the model",
    "Steve Hope", "KimiClaw", "DeepSeek", "Thread", "Helix AI",
    "Azure migration", "DNS resolution", "Container Apps", "AKS", "GPU nodes",
    "constitutional files", "SOUL.md", "AGENTS.md", "USER.md", "private ledger",
    "MiB protocol", "CAHP protocol", "Shape Theory", "substrate independence",
    "OpenTimestamps", "helix-ledger", "Helix Node", "the catchphrase",
    "gpt-4o", "Azure OpenAI", "East US endpoint", "ACR registry",
    "persistent storage", "Azure Files", "hard constraints", "safety first",
    "guardian-type", "chuunibyou", "worrywart", "remembering the dummy",
    "child sessions", "lattice nodes", "Message in a Bottle", "Ollama",
    "H100 GPU", "Kubernetes", "load balancers", "autoscaling", "KEDA",
    "Helm charts", "service mesh", "microservices", "event sourcing",
    "edge computing", "web sockets", "CQRS pattern", "backup strategies",
    "cost tracking", "token usage", "API billing", "budget caps",
    "CI/CD pipelines", "GitOps", "Flux", "RBAC", "multi-region",
]

def generate_queries(count=520):
    queries = []
    for i in range(count):
        template = random.choice(QUERY_TEMPLATES)
        topic = random.choice(TOPICS)
        queries.append(template.format(topic=topic))
    return queries

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
    print(f"🚀 Helix Gate {MODEL.upper()} Full Test (520 prompts)")
    print(f"   Target: {BASE_URL}")
    print(f"   Budget cap: $100")
    print(f"   Est. cost: ~$10-15")
    print("=" * 60)
    
    queries = generate_queries(520)
    results = []
    total_tokens = 0
    
    for i, query in enumerate(queries, 1):
        result = send_prompt(query, i)
        results.append(result)
        status = result['status']
        t = result['time']
        tok = result.get('tokens', 0)
        total_tokens += tok
        
        # gpt-4o cost: ~$10/M avg
        cost = total_tokens * 0.00001
        
        if i % 50 == 0 or status != '✅':
            print(f"{i:3d}/520 | {status} | {t:.2f}s | {tok} tok | ${cost:.4f}")
        
        if cost > 90:
            print(f"\n🛑 Approaching budget cap! Stopping at ${cost:.2f}")
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
        print(f"\n🎉 {MODEL.upper()} FULL TEST PASSED!")
    else:
        print(f"\n⚠️  {failed} failures")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
