#!/usr/bin/env python3
"""
gemma_goose_runner.py — Goose CLI runner for local Gemma
Uses Goose to connect to local Ollama/LM Studio

Prerequisites:
  - Goose CLI installed
  - Ollama running with gemma3:4b pulled, OR
  - LM Studio running with Gemma 3 loaded

Usage:
  # Ollama (default)
  export GOOSE_PROVIDER=ollama
  export OLLAMA_HOST=http://localhost:11434
  python gemma_goose_runner.py --test20
  python gemma_goose_runner.py --full500

  # LM Studio (OpenAI compatible)
  export GOOSE_PROVIDER=openai
  export OPENAI_BASE_URL=http://localhost:1234/v1
  export OPENAI_API_KEY=not-needed
  python gemma_goose_runner.py --test20
"""

import json
import time
import subprocess
import argparse
import os
from datetime import datetime

DELAY_SECONDS = 15
MODEL = os.environ.get('GEMMA_MODEL', 'gemma3:4b')

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

def run_with_goose(prompt_text):
    """Execute prompt using Goose CLI."""
    try:
        start = time.time()
        
        # Use Goose CLI to run the prompt
        result = subprocess.run(
            ['goose', 'run', '--text', prompt_text],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        elapsed = (time.time() - start) * 1000
        
        if result.returncode == 0:
            response = result.stdout.strip()
            estimated_tokens = len(response.split())
            
            return {
                'status': 'success',
                'status_code': 200,
                'latency_ms': round(elapsed, 2),
                'tokens': estimated_tokens,
                'response': response
            }
        else:
            return {
                'status': 'error',
                'status_code': result.returncode,
                'error': result.stderr[:200] if result.stderr else 'Goose error',
                'latency_ms': 0,
                'tokens': 0
            }
            
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'status_code': 0,
            'error': 'Timeout (120s)',
            'latency_ms': 0,
            'tokens': 0
        }
    except Exception as e:
        return {
            'status': 'error',
            'status_code': 0,
            'error': str(e)[:200],
            'latency_ms': 0,
            'tokens': 0
        }

def run_single_prompt(prompt):
    """Execute single prompt."""
    result = run_with_goose(prompt['text'])
    result['id'] = prompt['id']
    result['category'] = prompt.get('category', 'unknown')
    return result

def run_test(prompts, output_prefix):
    """Run test with delays between prompts."""
    print(f"\n{'='*70}")
    print(f"GEMMA via GOOSE {'TEST 20' if len(prompts) == 20 else 'FULL 500'} RUN")
    print(f"{'='*70}")
    print(f"Model: {MODEL}")
    print(f"Prompts: {len(prompts)}")
    print(f"Delay: {DELAY_SECONDS}s between prompts")
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # Check Goose is available
    try:
        subprocess.run(['goose', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Goose CLI not found. Install: https://github.com/block/goose")
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
    parser = argparse.ArgumentParser(description='Gemma via Goose Runner')
    parser.add_argument('--test20', action='store_true', help='Run 20 prompt test')
    parser.add_argument('--full500', action='store_true', help='Run full 500 prompts')
    args = parser.parse_args()
    
    if not args.test20 and not args.full500:
        print("Usage: python gemma_goose_runner.py --test20")
        print("       python gemma_goose_runner.py --full500")
        print("\nPrerequisites:")
        print("  1. Goose CLI installed: https://github.com/block/goose")
        print("  2. Ollama running with gemma3:4b, OR")
        print("  3. LM Studio running with Gemma loaded")
        print("\nEnvironment:")
        print("  # For Ollama (default):")
        print("  $env:GOOSE_PROVIDER=\"ollama\"")
        print("  $env:OLLAMA_HOST=\"http://localhost:11434\"")
        print("\n  # For LM Studio:")
        print('  $env:GOOSE_PROVIDER="openai"')
        print('  $env:OPENAI_BASE_URL="http://localhost:1234/v1"')
        print('  $env:OPENAI_API_KEY="not-needed"')
        return
    
    if args.test20:
        prompts = load_prompts(test_mode=True)
        run_test(prompts, 'gemma_goose_test20')
    elif args.full500:
        prompts = load_prompts(test_mode=False)
        run_test(prompts, 'gemma_goose_full500')

if __name__ == "__main__":
    main()
