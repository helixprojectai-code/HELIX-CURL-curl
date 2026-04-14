#!/usr/bin/env python3
"""
gpt4o_mini_prerun_20.py — Pre-run 20 prompt test
Validates keys, timeouts, connectivity before full 500 run
"""

import json
import time
import urllib.request
import urllib.error
from datetime import datetime

# Goose Gate Configuration
GOOSE_GATE_URL = "https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io/api/v1/chat"
API_KEY = "TnXYS82EgRDabPbWHRpgwuCuReMvkG9OFN9fP4fKCFk="
MODEL = "gpt-4o-mini"

def load_prompts():
    with open('data/prompts/prompts_500.json', 'r') as f:
        all_prompts = json.load(f)
    # Select 20 representative prompts
    test_ids = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475]
    return [p for p in all_prompts if p['id'] in test_ids]

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
                'status': 'success',
                'latency_ms': round(elapsed, 2),
                'tokens': tokens,
                'response_preview': content[:100] + '...' if len(content) > 100 else content
            }
    except urllib.error.HTTPError as e:
        return {
            'id': prompt['id'],
            'status': 'error',
            'error': f"HTTP {e.code}: {e.read().decode('utf-8')[:100]}"
        }
    except Exception as e:
        return {
            'id': prompt['id'],
            'status': 'error',
            'error': str(e)[:100]
        }

def main():
    print("="*70)
    print("GPT-4o MINI PRE-RUN 20 PROMPT TEST")
    print("="*70)
    print(f"Endpoint: {GOOSE_GATE_URL}")
    print(f"Model: {MODEL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*70)
    
    prompts = load_prompts()
    print(f"\nLoaded {len(prompts)} test prompts\n")
    
    results = []
    for i, prompt in enumerate(prompts):
        result = run_single_prompt(prompt)
        results.append(result)
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"{status} [{i+1:2d}/20] ID:{result['id']:3d} ({result.get('latency_ms', 0):6.0f}ms)")
    
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
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'results/prerun_20_{timestamp}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return success_count

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success >= 18 else 1)
