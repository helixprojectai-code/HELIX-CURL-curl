#!/usr/bin/env python3
"""
gemma_lmstudio_runner.py — Direct LM Studio API runner for Gemma
Uses LM Studio's built-in OpenAI-compatible server

Prerequisites:
  - LM Studio running with Gemma 3 loaded
  - Server started (click "Start Server" in LM Studio)

Usage:
  # Default (localhost:1234)
  python gemma_lmstudio_runner.py --test20
  python gemma_lmstudio_runner.py --full500

  # Custom host/port
  $env:LMSTUDIO_URL="http://localhost:1234/v1"
  python gemma_lmstudio_runner.py --test20
"""

import json
import time
import urllib.request
import urllib.error
import argparse
import os
from datetime import datetime

# Configuration
LMSTUDIO_URL = os.environ.get('LMSTUDIO_URL', 'http://localhost:1234/v1')
MODEL = os.environ.get('GEMMA_MODEL', 'google/gemma-3n-e4b')  # LM Studio model name
DELAY_SECONDS = 15

def load_prompts(test_mode=False):
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
                
            if test_mode:
                test_ids = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 
                           250, 275, 300, 325, 350, 375, 400, 425, 450, 475]
                return [p for p in all_prompts if p['id'] in test_ids]
            else:
                return all_prompts
    
    raise FileNotFoundError("Could not find prompts_500.json")

def run_single_prompt(prompt):
    """Execute single prompt via LM Studio API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer not-needed"  # LM Studio doesn't check this
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt['text']}],
        "temperature": 1.0,
        "max_tokens": 500,
        "stream": False
    }
    
    start = time.time()
    try:
        req = urllib.request.Request(
            f"{LMSTUDIO_URL}/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=120) as response:
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

def run_test(prompts, output_prefix):
    """Run test with delays between prompts."""
    print(f"\n{'='*70}")
    print(f"GEMMA via LM STUDIO {'TEST 20' if len(prompts) == 20 else 'FULL 500'} RUN")
    print(f"{'='*70}")
    print(f"Endpoint: {LMSTUDIO_URL}")
    print(f"Model: {MODEL}")
    print(f"Prompts: {len(prompts)}")
    print(f"Delay: {DELAY_SECONDS}s between prompts")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # Check LM Studio is reachable
    try:
        req = urllib.request.Request(f"{LMSTUDIO_URL}/models", method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            print("✅ LM Studio server reachable\n")
    except Exception as e:
        print(f"⚠️  LM Studio not responding: {e}")
        print("\nMake sure:")
        print("  1. LM Studio is running")
        print("  2. Gemma 3 model is loaded")
        print("  3. Server is started (click 'Start Server')")
        return
    
    results = []
    for i, prompt in enumerate(prompts):
        result = run_single_prompt(prompt)
        results.append(result)
        
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"{status} [{i+1:3d}/{len(prompts)}] ID:{result['id']:3d} ({result.get('latency_ms', 0):6.0f}ms)")
        
        if i < len(prompts) - 1:
            time.sleep(DELAY_SECONDS)
    
    # Summary
    success = sum(1 for r in results if r['status'] == 'success')
    errors = sum(1 for r in results if r['status'] == 'error')
    success_results = [r for r in results if r['status'] == 'success']
    avg_latency = sum(r['latency_ms'] for r in success_results) / max(len(success_results), 1)
    total_tokens = sum(r['tokens'] for r in success_results)
    
    print(f"\n{'='*70}")
    print("RUN COMPLETE")
    print(f"{'='*70}")
    print(f"Success: {success}/{len(prompts)} ({100*success/len(prompts):.1f}%)")
    print(f"Errors:  {errors}/{len(prompts)} ({100*errors/len(prompts):.1f}%)")
    print(f"Avg latency: {avg_latency:.0f}ms")
    print(f"Total tokens: {total_tokens:,}")
    print(f"End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'results/{output_prefix}_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved: {output_file}")
    return results

def main():
    parser = argparse.ArgumentParser(description='Gemma via LM Studio Runner')
    parser.add_argument('--test20', action='store_true', help='Run 20 prompt test')
    parser.add_argument('--full500', action='store_true', help='Run full 500 prompts')
    args = parser.parse_args()
    
    if not args.test20 and not args.full500:
        print("Usage: python gemma_lmstudio_runner.py --test20")
        print("       python gemma_lmstudio_runner.py --full500")
        print("\nPrerequisites:")
        print("  1. LM Studio running")
        print("  2. Gemma 3 model loaded")
        print("  3. Server started (click 'Start Server' button)")
        print("\nDefault URL: http://localhost:1234/v1")
        print("\nTo customize:")
        print('  $env:LMSTUDIO_URL="http://localhost:1234/v1"')
        return
    
    if args.test20:
        prompts = load_prompts(test_mode=True)
        run_test(prompts, 'gemma_lmstudio_test20')
    elif args.full500:
        prompts = load_prompts(test_mode=False)
        run_test(prompts, 'gemma_lmstudio_full500')

if __name__ == "__main__":
    main()
