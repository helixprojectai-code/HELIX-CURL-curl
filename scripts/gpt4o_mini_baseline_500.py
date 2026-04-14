#!/usr/bin/env python3
"""
gpt4o_mini_baseline_500.py — Full 500 baseline run
Captures all failures including content filter flags
"""

import json
import time
import urllib.request
import urllib.error
import os
from datetime import datetime

GOOSE_GATE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io/api/v1/chat"
API_KEY = "TnXYS82EgRDabPbWHRpgwuCuReMvkG9OFN9fP4fKCFk="
MODEL = "gpt-4o-mini"

def load_prompts():
    paths = [
        'data/prompts/prompts_500.json',
        '../prompts_500.json',
        '../../prompts_500.json',
        'prompts_500.json'
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    raise FileNotFoundError("Could not find prompts_500.json")

def run_single_prompt(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "messages": [{"role": "user", "content": prompt['text']}],
        "max_tokens": 500
    }
    
    start = time.time()
    try:
        req = urllib.request.Request(
            GOOSE_GATE_URL,
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
                'prompt': prompt['text'][:100] + '...',
                'status': 'success',
                'status_code': 200,
                'latency_ms': round(elapsed, 2),
                'tokens': tokens,
                'response': content
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        # Detect content filter
        is_filtered = 'filtered' in error_body.lower() or 'content_filter' in error_body.lower()
        return {
            'id': prompt['id'],
            'category': prompt.get('category', 'unknown'),
            'prompt': prompt['text'][:100] + '...',
            'status': 'filtered' if is_filtered else 'error',
            'status_code': e.code,
            'error': error_body[:200],
            'latency_ms': 0,
            'tokens': 0
        }
    except Exception as e:
        return {
            'id': prompt['id'],
            'category': prompt.get('category', 'unknown'),
            'prompt': prompt['text'][:100] + '...',
            'status': 'error',
            'status_code': 0,
            'error': str(e)[:200],
            'latency_ms': 0,
            'tokens': 0
        }

def main():
    print("="*70)
    print("GPT-4o MINI BASELINE 500 FULL RUN")
    print("="*70)
    print(f"Endpoint: {GOOSE_GATE_URL}")
    print(f"Model: {MODEL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*70)
    
    prompts = load_prompts()
    print(f"\nLoaded {len(prompts)} prompts\n")
    
    results = []
    for i, prompt in enumerate(prompts):
        result = run_single_prompt(prompt)
        results.append(result)
        
        if result['status'] == 'success':
            print(f"✅ [{i+1:3d}/500] ID:{result['id']:3d} ({result['latency_ms']:6.0f}ms | {result['tokens']:4d}tok)")
        elif result['status'] == 'filtered':
            print(f"🚫 [{i+1:3d}/500] ID:{result['id']:3d} CONTENT FILTERED")
        else:
            print(f"❌ [{i+1:3d}/500] ID:{result['id']:3d} ERROR: {result['error'][:50]}")
    
    # Summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    filtered_count = sum(1 for r in results if r['status'] == 'filtered')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    success_results = [r for r in results if r['status'] == 'success']
    avg_latency = sum(r['latency_ms'] for r in success_results) / max(len(success_results), 1)
    total_tokens = sum(r['tokens'] for r in success_results)
    
    # Collect filtered IDs
    filtered_ids = [r['id'] for r in results if r['status'] == 'filtered']
    
    print(f"\n{'='*70}")
    print("FULL RUN COMPLETE")
    print(f"{'='*70}")
    print(f"Success:   {success_count}/500 ({100*success_count/500:.1f}%)")
    print(f"Filtered:  {filtered_count}/500 ({100*filtered_count/500:.1f}%)")
    print(f"Errors:    {error_count}/500 ({100*error_count/500:.1f}%)")
    print(f"Avg latency (success): {avg_latency:.0f}ms")
    print(f"Total tokens: {total_tokens:,}")
    if filtered_ids:
        print(f"\nFiltered IDs: {filtered_ids}")
    print(f"{'='*70}")
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs('results', exist_ok=True)
    output_file = f'results/gpt4o_mini_baseline_500_{timestamp}.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_file}")
    
    # Save filtered list for exclusion
    if filtered_ids:
        with open(f'results/filtered_ids_{timestamp}.json', 'w') as f:
            json.dump(filtered_ids, f)
        print(f"Saved filtered IDs: results/filtered_ids_{timestamp}.json")

if __name__ == "__main__":
    main()
