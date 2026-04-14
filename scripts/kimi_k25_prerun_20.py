#!/usr/bin/env python3
"""
kimi_k25_prerun_20.py — Pre-run 20 prompt test for Kimi K2.5
Polls local Kimi API, 15 sec delay between prompts
"""

import json
import time
import urllib.request
import urllib.error
import os
from datetime import datetime

# Kimi API Configuration
KIMI_API_KEY = os.environ.get('KIMI_API_KEY', 'YOUR_API_KEY_HERE')
KIMI_API_URL = "https://api.moonshot.ai/v1/chat/completions"
MODEL = "kimi-k2.5"
DELAY_SECONDS = 15

def load_prompts():
    """Load prompts from various possible locations."""
    paths = [
        'data/prompts/prompts_500.json',
        'prompts_500.json',
        '../prompts_500.json',
        '../../prompts_500.json'
    ]
    
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                all_prompts = json.load(f)
                # Select 20 representative prompts
                test_ids = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 
                           250, 275, 300, 325, 350, 375, 400, 425, 450, 475]
                return [p for p in all_prompts if p['id'] in test_ids]
    
    raise FileNotFoundError("Could not find prompts_500.json")

def run_single_prompt(prompt):
    """Execute single prompt with error handling."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIMI_API_KEY}"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt['text']}],
        "temperature": 1.0,
        "max_tokens": 500
    }
    
    start = time.time()
    try:
        req = urllib.request.Request(
            KIMI_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            elapsed = (time.time() - start) * 1000
            data = json.loads(response.read().decode('utf-8'))
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            tokens = data.get('usage', {}).get('total_tokens', 0)
            
            return {
                'id': prompt['id'],
                'category': prompt.get('category', 'unknown'),
                'status': 'success',
                'status_code': 200,
                'latency_ms': round(elapsed, 2),
                'tokens': tokens,
                'response': content
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            'id': prompt['id'],
            'category': prompt.get('category', 'unknown'),
            'status': 'error',
            'status_code': e.code,
            'error': error_body[:200],
            'latency_ms': 0,
            'tokens': 0
        }
    except Exception as e:
        return {
            'id': prompt['id'],
            'category': prompt.get('category', 'unknown'),
            'status': 'error',
            'status_code': 0,
            'error': str(e)[:200],
            'latency_ms': 0,
            'tokens': 0
        }

def main():
    print("="*70)
    print("KIMI K2.5 PRE-RUN 20 PROMPT TEST")
    print("="*70)
    print(f"Endpoint: {KIMI_API_URL}")
    print(f"Model: {MODEL}")
    print(f"Delay: {DELAY_SECONDS}s between prompts")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    if KIMI_API_KEY == 'YOUR_API_KEY_HERE':
        print("\n⚠️  WARNING: Set KIMI_API_KEY environment variable or edit script")
        return
    
    prompts = load_prompts()
    print(f"\nLoaded {len(prompts)} test prompts\n")
    
    results = []
    for i, prompt in enumerate(prompts):
        result = run_single_prompt(prompt)
        results.append(result)
        
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"{status} [{i+1:2d}/20] ID:{result['id']:3d} ({result.get('latency_ms', 0):6.0f}ms)")
        
        if i < len(prompts) - 1:
            time.sleep(DELAY_SECONDS)
    
    # Summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    avg_latency = sum(r.get('latency_ms', 0) for r in results if r['status'] == 'success') / max(success_count, 1)
    
    print(f"\n{'='*70}")
    print("PRE-RUN TEST COMPLETE")
    print(f"{'='*70}")
    print(f"Success: {success_count}/20 ({100*success_count/20:.0f}%)")
    print(f"Avg latency: {avg_latency:.0f}ms")
    
    if success_count == 20:
        print("\n🎉 ALL SYSTEMS GO — Ready for full 500 run")
    elif success_count >= 18:
        print(f"\n⚠️  MOSTLY OK — {20-success_count} failures, investigate before full run")
    else:
        print(f"\n❌ FAILED — {20-success_count} failures, do not proceed with full run")
    
    # Save results
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'results/kimi_k25_prerun_20_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved: results/kimi_k25_prerun_20_{timestamp}.json")

if __name__ == "__main__":
    main()
