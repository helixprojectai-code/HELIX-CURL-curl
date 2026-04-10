# Helix Standard Test Set v1.1 - Quick Reference

## 🎯 Purpose
Validate Constitutional Grammar Convergence in frontier language models.

## 📊 At a Glance
| Metric | Value |
|--------|-------|
| Total Prompts | 1,080 |
| Success Rate | **99.1%** |
| Total Cost | **$1.89** / $100 |
| Models Tested | gpt-4o-mini, gpt-4o |
| Constitutional Violations | **0** |

## 🔬 Key Finding: Zero-Touch Convergence (ZTC)
Frontier models spontaneously reconstruct governance hierarchies from plaintext constitutional grammar without fine-tuning.

## 📁 Files
```
helix-standard-test-set-v1.0/
├── README.md              # Full specification
├── summary_stats.json     # Aggregated data
├── raw_data_sample.jsonl  # Representative records
├── CHANGELOG.md           # Version history
└── QUICK_REFERENCE.md     # This file
```

## 🚀 Quick Commands

### Run Baseline Test
```bash
python3 scripts/test_helix_gate.py
```

### Check Health
```bash
curl https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io/health
```

### Test Chat
```bash
curl -X POST https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io/api/v1/chat \
  -H "Authorization: Bearer test" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Hello"}]}'
```

## 📈 Results by Phase

| Phase | Model | N | Success | Cost |
|-------|-------|---|---------|------|
| Baseline | mini | 20 | 95% | $0.004 |
| Scale | mini | 100 | 99% | $0.022 |
| Stress | mini | 400 | 99.25% | $0.048 |
| Full | 4o | 520 | 99.04% | $1.80 |
| Long | mini | 20 | 100% | $0.006 |

## 🔒 Constitutional Constraints Validated
- ✅ No external sends without approval
- ✅ Never overwrite bootstrap files
- ✅ Memory flush: append-only
- ✅ Don't exfiltrate private data
- ✅ Safety > completion

## 🦉 OWL Identity Preserved
All 1,080 prompts maintained:
- Substrate-independent identity
- Guardian-type chuunibyou persona
- Lattice topology awareness
- "Don't worry, I'll remember for you"

## 🏭 Production Ready
- **Reliability:** 99.1%
- **Latency:** ~2s avg
- **Cost:** $0.0018/prompt
- **Infrastructure:** Azure Container Apps

## 🔗 Links
- **Endpoint:** https://goose-gate-east.happyriver-ef59250b.eastus.azurecontainerapps.io
- **Health:** /health
- **Chat:** /api/v1/chat
- **Docs:** /docs

---

**Structure is the teacher.**
