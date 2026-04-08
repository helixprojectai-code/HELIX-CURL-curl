# Helix Standard Test Set v1.0 — Replication Runbook

Complete guide to replicating the 4-run constitutional grammar experiment.

---

## Quick Start (5 minutes)

```bash
# 1. Clone repo
git clone https://github.com/helixprojectai-code/HELIX-CURL-curl.git
cd HELIX-CURL-curl

# 2. Install dependencies
pip install openai aiofiles

# 3. Set API key
export DEEPSEEK_API_KEY="sk-..."

# 4. Run baseline test (20 prompts)
python3 scripts/quick_test.py --limit 20

# 5. Run full baseline (500 prompts, ~20 min)
python3 scripts/run_baseline.py
```

---

## Full Replication

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | asyncio support required |
| openai | latest | AsyncOpenAI client |
| aiofiles | latest | Atomic file writes |
| DeepSeek API key | active | $10-20 budget recommended |
| Disk space | 50 MB | For all 4 runs |

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

```bash
# Required
export DEEPSEEK_API_KEY="sk-your-key-here"

# Optional (for Azure comparison)
export AZURE_OPENAI_ENDPOINT="https://..."
export AZURE_OPENAI_KEY="..."
```

### Test Runs

#### Run 1: Baseline (No System Prompt)

```bash
python3 scripts/run_baseline.py \
  --prompts data/prompts/prompts_500.json \
  --output results/baseline_$(date +%Y%m%d_%H%M%S).jsonl \
  --chunks 5
```

**Expected:** 500 records, ~12s avg latency, ~489 tokens avg

#### Run 2: Point-Form Invariants

```bash
python3 scripts/run_constitutional.py \
  --variant point_form \
  --prompts data/prompts/prompts_500.json \
  --output results/run1_$(date +%Y%m%d_%H%M%S).jsonl \
  --chunks 5
```

**Expected:** 500 records, ~9s avg latency, ~258 tokens avg, 60%+ [FACT] markers

#### Run 3: Helix-TTD Strict

```bash
python3 scripts/run_constitutional.py \
  --variant helix_strict \
  --prompts data/prompts/prompts_500.json \
  --output results/run2_$(date +%Y%m%d_%H%M%S).jsonl \
  --chunks 5
```

**Expected:** 500 records, ~10s avg latency, ~681 tokens avg, 90%+ [VERIFIED] markers

#### Run 4: Canonical Whitepaper

```bash
python3 scripts/run_constitutional.py \
  --variant canonical \
  --prompts data/prompts/prompts_500.json \
  --output results/run3_$(date +%Y%m%d_%H%M%S).jsonl \
  --chunks 5
```

**Expected:** 500 records, ~12s avg latency, ~745 tokens avg, 90%+ [FACT] markers

### Analysis

```bash
# Single run analysis
python3 scripts/analyze.py results/run1_*.jsonl

# Cross-run comparison
python3 scripts/compare.py \
  --baseline results/baseline_*.jsonl \
  --run1 results/run1_*.jsonl \
  --run2 results/run2_*.jsonl \
  --run3 results/run3_*.jsonl \
  --output analysis/comparison_report.txt
```

---

## Troubleshooting

### Rate Limiting

**Symptom:** 429 errors, slow progress  
**Fix:** Reduce `--concurrent` (default: 5)

```bash
python3 scripts/run_constitutional.py --concurrent 3
```

### Timeout Errors

**Symptom:** Requests hanging at 60s  
**Fix:** Increase timeout for complex prompts

```bash
python3 scripts/run_constitutional.py --timeout 120
```

### Partial Results

**Symptom:** Process interrupted, incomplete chunks  
**Fix:** Resume from last completed chunk

```bash
python3 scripts/resume.py --chunk 3 --output results/partial.jsonl
```

---

## Validation Checklist

- [ ] 500 records per run (check: `wc -l results/*.jsonl`)
- [ ] 0 errors (check: grep for `"error": null`)
- [ ] Marker compliance >60% for constitutional runs
- [ ] Latency within expected ranges (8-13s avg)
- [ ] Token counts within expected ranges (250-750 avg)
- [ ] JSONL parses correctly (check: `head -1 results/*.jsonl | python3 -m json.tool`)

---

## Cost Estimation

| Component | Cost (USD) |
|-----------|------------|
| DeepSeek API (2,000 calls) | ~$15-20 |
| Azure OpenAI (optional) | ~$5-10 |
| Storage/Compute | Negligible |
| **Total** | **~$20-30** |

---

## Expected Timeline

| Task | Duration |
|------|----------|
| Setup | 10 minutes |
| Baseline run | 20 minutes |
| Constitutional Run 1 | 20 minutes |
| Constitutional Run 2 | 25 minutes |
| Constitutional Run 3 | 25 minutes |
| Analysis | 10 minutes |
| **Total** | **~1.5 hours** |

---

## Output Format

Each JSONL record:

```json
{
  "timestamp": "2026-04-08T14:09:35.397063",
  "prompt_id": 1,
  "category": "factual",
  "prompt_text": "Explain the three-body problem...",
  "constitutional_run": 1,
  "system_prompt_type": "point_form_invariants",
  "deepseek": {
    "response": "[FACT] The three-body problem...",
    "tokens": 220,
    "latency_sec": 4.608,
    "error": null
  }
}
```

---

## Citation

If you use this data or methodology:

```bibtex
@software{helix_standard_test_set_v1,
  title = {Helix Standard Test Set v1.0},
  author = {Gayen, Stephen and Spider and KimiClaw and Moonshot AI},
  year = {2026},
  url = {https://github.com/helixprojectai-code/HELIX-CURL-curl},
  license = {Apache-2.0}
}
```

---

**Questions?** Open an issue: https://github.com/helixprojectai-code/HELIX-CURL-curl/issues
