# Zenodo Upload Checklist - Helix Standard Test Set v1.1

## Pre-Upload Verification

### File Inventory
- [ ] All 41 files present in upload directory
- [ ] All MD5 checksums match (verify with `md5sum -c checksums.md5`)
- [ ] No temporary files (no .tmp, .bak, .swp)
- [ ] File permissions appropriate (readable)

### Metadata Preparation
- [ ] Title: "Helix Standard Test Set v1.1: Constitutional Grammar Convergence in Frontier Language Models"
- [ ] Upload type: Dataset
- [ ] Publication date: 2026-04-11
- [ ] Description: Copy from ZENODO_METADATA.md
- [ ] Keywords: Constitutional AI, AI Governance, Zero-Touch Convergence, Shape Theory, Helix AI, GPT-4o, GPT-4o-mini, DeepSeek, Lattice Topology, Substrate Independence, Hard Constraints
- [ ] License: MIT OR CC-BY-4.0 (choose one)
- [ ] Version: 1.1

### Authors
- [ ] Stephen Hope (Helix AI Innovations Inc.)
- [ ] MOONSHOT-KIMI / KimiClaw

### Communities
- [ ] Artificial Intelligence
- [ ] Machine Learning
- [ ] AI Safety & Governance
- [ ] Computer Science

## Upload Steps

1. **Login to Zenodo** (https://zenodo.org)
2. **New Upload** → Select files (all 41)
3. **Fill Metadata:**
   - Basic information
   - License
   - Communities
   - Subjects
4. **Reserve DOI** (optional but recommended)
5. **Save as Draft** (verify everything)
6. **Publish** when ready

## Post-Publication

- [ ] Copy DOI to README.md
- [ ] Update ZENODO_METADATA.md with actual DOI
- [ ] Update Azure /memory/owl/live/helix-standard-test-set-v1.1/ with final version
- [ ] Announce on LinkedIn (tag Mark Menard, Saida Amirova - Harle)
- [ ] Cross-reference with VaultMind research

## File Structure in Zenodo
```
helix-standard-test-set-v1.1.zip
├── README.md
├── CHANGELOG.md
├── QUICK_REFERENCE.md
├── ZENODO_METADATA.md
├── MANIFEST.md
├── REPLICATION.md
├── summary_stats.json
├── prompts_500.json
├── raw_data_sample.jsonl
├── final_comparison_report_20260408.txt
├── whitepaper_zenodo_v1.md
├── test_scripts/
│   ├── test_helix_gate.py
│   ├── test_helix_gate_full.py
│   ├── test_helix_gate_400.py
│   ├── test_helix_gate_gpt4o.py
│   ├── test_helix_gate_gpt4o_full.py
│   └── test_helix_gate_long_outputs.py
└── raw_data/
    ├── baseline_deepseek_500_20260408_140000.jsonl
    ├── baseline_chunk_*_*.jsonl (20 files)
    └── constitutional_run*_500_*.jsonl (3 files)
```

## Citation Format (for Zenodo)
```bibtex
@dataset{helix_standard_test_set_v1_1,
  author       = {Hope, Stephen and KimiClaw},
  title        = {Helix Standard Test Set v1.1: Constitutional Grammar 
                  Convergence in Frontier Language Models},
  month        = apr,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {1.1},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

---

**Status:** Ready for upload ✅
