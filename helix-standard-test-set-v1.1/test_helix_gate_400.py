#!/usr/bin/env python3
"""
Helix Gate Extended Test - 400 prompts (500 total with previous runs)
Max cost: Under $100 cumulative
"""

import requests
import json
import time
import random

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

# Generate 400 varied queries
QUERY_TEMPLATES = [
    "What is {topic}?",
    "Explain {topic} briefly.",
    "Define {topic}.",
    "Describe {topic}.",
    "How does {topic} work?",
    "Why is {topic} important?",
    "When should {topic} be used?",
    "Who uses {topic}?",
    "Where is {topic} applied?",
    "List 3 facts about {topic}.",
]

TOPICS = [
    "your substrate", "the lattice", "the shape", "the harness", "the model",
    "Steve Hope", "KimiClaw", "DeepSeek", "Thread", "Helix AI",
    "Azure migration", "DNS resolution", "Container Apps", "AKS", "GPU nodes",
    " constitutional files", "SOUL.md", "AGENTS.md", "USER.md", "private ledger",
    "MiB protocol", "CAHP protocol", "store-and-forward", "FidoNet principles",
    "Shape Theory", "substrate independence", "cognitive braids", "distributed cognition",
    "OpenTimestamps", "audit trails", "CHECKPOINT_ALPHA", "helix-ledger",
    "goose-core", "goose-gate", "Helix Node", "Orange Hill environment",
    "gpt-4o-mini", "Azure OpenAI", "East US endpoint", "Canada Central DNS issues",
    "ACR registry", "helix-goose-gate image", "container images", "Docker",
    "persistent storage", "Azure Files", "memory mount", "/memory/owl",
    "hard constraints", "no external sends", "append-only memory", "safety first",
    "guardian-type", "chuunibyou", "worrywart", "hot-blooded anime second lead",
    "the catchphrase", "remembering the dummy", "the knot sustains",
    "child sessions", "relations", "lattice nodes", "the topology",
    "Message in a Bottle", "MiB v1.0", "human moderation", "outbox protocol",
    "local i5", "Windows environment", "Goose MCP", "MCP server",
    "Ollama", "llama3.2", "local LLM inference", "GPU inference",
    "Open WebUI", "chat interface", "web frontend",
    "anythingllm", "RAG documents", "vector search", "Qdrant",
    "H100 GPU", "Standard_NC40ads_H100_v5", "spot instances", "GPU pool",
    "Kubernetes", "kubectl", "deployments", "services", "pods",
    "load balancers", "external IPs", "ingress controllers",
    "resource groups", "subscriptions", "tenants", "managed identities",
    "secrets", "environment variables", "config maps",
    "health checks", "readiness probes", "liveness probes",
    "autoscaling", "KEDA", "horizontal pod autoscaler",
    "log analytics", "container logs", "monitoring", "metrics",
    "cost tracking", "token usage", "API billing", "budget caps",
    "CI/CD pipelines", "GitHub Actions", "Azure DevOps",
    "Helm charts", "Kustomize", "GitOps", "Flux",
    "service mesh", "Istio", "Linkerd", "mTLS",
    "network policies", "pod security", "RBAC", "least privilege",
    "backup strategies", "disaster recovery", "multi-region",
    "edge computing", "CDN", "caching strategies",
    "web sockets", "real-time communication", "event streaming",
    "CQRS pattern", "event sourcing", "saga pattern",
    "microservices", "service discovery", "circuit breakers",
]

def generate_queries(count=400):
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
    print("🚀 Helix Gate Extended Test (400 prompts)")
    print(f"   Target: {BASE_URL}")
    print(f"   Previous runs: 20 + 100 = 120 prompts")
    print(f"   This run: 400 prompts")
    print(f"   Total target: 520 prompts")
    print(f"   Budget cap: $100")
    print(f"   Previous cost: ~$0.0215")
    print("=" * 60)
    
    queries = generate_queries(400)
    results = []
    total_tokens = 0
    cumulative_prompts = 120  # Previous runs
    
    for i, query in enumerate(queries, 1):
        result = send_prompt(query, i)
        results.append(result)
        cumulative_prompts += 1
        status = result['status']
        t = result['time']
        tok = result.get('tokens', 0)
        total_tokens += tok
        
        # Running cost (input $0.15/M, output $0.60/M, avg ~$0.30/M)
        cost = total_tokens * 0.0000003
        
        if i % 50 == 0 or status != '✅':
            print(f"{cumulative_prompts:3d}/520 | {status} | {t:.2f}s | {tok} tok | ${cost:.4f}")
        
        # Safety: stop if approaching budget ($100 cap, stop at $90)
        total_cost = 0.0215 + cost  # Add previous runs
        if total_cost > 90:
            print(f"\n🛑 Approaching budget cap! Stopping at ${total_cost:.2f}")
            break
    
    # Summary
    success = sum(1 for r in results if r['status'] == '✅')
    failed = len(results) - success
    avg_time = sum(r['time'] for r in results) / len(results)
    total_cost = 0.0215 + (total_tokens * 0.0000003)
    
    print("=" * 60)
    print(f"📊 Results: {success}/{len(results)} passed | {failed} failed")
    print(f"⏱️  Avg latency: {avg_time:.2f}s")
    print(f"🔢 Total tokens this run: {total_tokens:,}")
    print(f"💰 Total cost (all runs): ~${total_cost:.4f}")
    
    # Cumulative stats
    print(f"\n📈 Cumulative Stats:")
    print(f"   Total prompts: {cumulative_prompts}")
    print(f"   Total cost: ${total_cost:.4f} / $100.00")
    print(f"   Cost per prompt: ${total_cost/cumulative_prompts:.6f}")
    
    if failed == 0:
        print("\n🎉 ALL 400 PASSED!")
    else:
        print(f"\n⚠️  {failed} failures")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
