#!/usr/bin/env python3
"""
gemma_baseline_500.py — Full 500 baseline run for Gemma 3
Polls local Ollama API, 15 sec delay between prompts, inline execution
"""

import json
import time
import urllib.request
import urllib.error
import os
from datetime import datetime

# Ollama Configuration
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
MODEL = os.environ.get('GEMMA_MODEL', 'gemma3:4b')
DELAY_SECONDS = 15

# Output files
OUTPUT_FILE = "gemma_baseline_results.json"
CHECKPOINT_FILE = "gemma_baseline_checkpoint.json"

def load_prompts():
    """Load the 500-prompt test set."""
    paths = [
        'data/prompts/prompts_500.json',
        'prompts_500.json',
        '../prompts_500.json',
        '../../prompts_500.json'
    ]
    
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    raise FileNotFoundError("Could not find prompts_500.json")

def load_checkpoint():
    """Load progress from checkpoint if exists."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_checkpoint(results):
    """Save progress to checkpoint."""
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

def run_single_prompt(prompt):
    """Execute single prompt with error handling."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "prompt": prompt['text'],
        "stream": False,
        "options": {"temperature": 1.0}
    }
    
    start = time.time()
    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=120) as response:
            elapsed = (time.time() - start) * 1000
            data = json.loads(response.read().decode('utf-8'))
            content = data.get('response', '')
            estimated_tokens = len(content.split())
            
            return {
                'id': prompt['id'],
                'category': prompt.get('category', 'unknown'),
                'prompt': prompt['text'][:100] + '...',
                'status': 'success',
                'status_code': 200,
                'latency_ms': round(elapsed, 2),
                'tokens': estimated_tokens,
                'response': content
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            'id': prompt['id'],
            'category': prompt.get('category', 'unknown'),
            'prompt': prompt['text'][:100] + '...',
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
            'prompt': prompt['text'][:100] + '...',
            'status': 'error',
            'status_code': 0,
            'error': str(e)[:200],
            'latency_ms': 0,
            'tokens': 0
        }

def main():
    print("="*70)
    print("GEMMA 3 BASELINE 500 FULL RUN")
    print("="*70)
    print(f"Endpoint: {OLLAMA_URL}")
    print(f"Model: {MODEL}")
    print(f"Delay: {DELAY_SECONDS}s between prompts")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    print(f"\nEnvironment setup:")
    print(f"  CMD: set OLLAMA_URL=http://localhost:11434")
    print(f"  PS: $env:OLLAMA_URL=\"http://localhost:11434\"")
    print(f"  CMD: set GEMMA_MODEL=gemma3:4b")
    print(f"  PS: $env:GEMMA_MODEL=\"gemma3:4b\"")
    print()
    
    # Load prompts and checkpoint
    all_prompts = load_prompts()
    completed_results = load_checkpoint()
    completed_ids = {r['id'] for r in completed_results}
    
    # Filter to remaining prompts
    remaining = [p for p in all_prompts if p['id'] not in completed_ids]
    
    print(f"Total prompts: {len(all_prompts)}")
    print(f"Already completed: {len(completed_results)}")
    print(f"Remaining: {len(remaining)}")
    print(f"Estimated time: ~{(len(remaining) * (DELAY_SECONDS + 5)) / 60:.0f} minutes\n")
    
    results = completed_results.copy()
    
    for i, prompt in enumerate(remaining):
        overall_idx = len(completed_results) + i
        result = run_single_prompt(prompt)
        results.append(result)
        
        if result['status'] == 'success':
            print(f"✅ [{overall_idx+1:3d}/500] ID:{result['id']:3d} ({result['latency_ms']:6.0f}ms)")
        else:
            print(f"❌ [{overall_idx+1:3d}/500] ID:{result['id']:3d} ERROR: {result['error'][:50]}")
        
        # Save checkpoint every 10 prompts
        if (i + 1) % 10 == 0:
            save_checkpoint(results)
            print(f"    💾 Checkpoint saved ({len(results)}/500)")
        
        # Delay before next prompt
        if i < len(remaining) - 1:
            time.sleep(DELAY_SECONDS)
    
    # Final summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] == 'error')
    success_results = [r for r in results if r['status'] == 'success']
    avg_latency = sum(r['latency_ms'] for r in success_results) / max(len(success_results), 1)
    
    print(f"\n{'='*70}")
    print("RUN COMPLETE")
    print(f"{'='*70}")
    print(f"Success: {success_count}/500 ({100*success_count/500:.1f}%)")
    print(f"Errors:  {error_count}/500 ({100*error_count/500:.1f}%)")
    print(f"Avg latency: {avg_latency:.0f}ms")
    print(f"End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    # Save final results
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'results/gemma_baseline_500_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Clean up checkpoint
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
    
    print(f"\nSaved: {output_file}")
    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
