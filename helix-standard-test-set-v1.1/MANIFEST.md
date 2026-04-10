# Helix Standard Test Set v1.1 - Complete File Manifest

## Documentation (5 files)
| File | Size | Description |
|------|------|-------------|
| README.md | 7.71 KB | Full specification, ZTC findings, methodology |
| CHANGELOG.md | 2.52 KB | Version history v1.0 → v1.1 |
| QUICK_REFERENCE.md | 2.41 KB | At-a-glance summary |
| ZENODO_METADATA.md | 3.56 KB | Publication metadata for Zenodo |
| MANIFEST.md | 2.1 KB | This file - complete inventory |
| REPLICATION.md | 5.11 KB | Replication guide for independent verification |

## Test Scripts - Reproducibility (6 files)
| File | Lines | Purpose |
|------|-------|---------|
| test_helix_gate.py | ~150 | Baseline 20-prompt test |
| test_helix_gate_full.py | ~180 | Full 520-prompt test (mini) |
| test_helix_gate_400.py | ~180 | Extended 400-prompt stress test |
| test_helix_gate_gpt4o.py | ~130 | GPT-4o 20-prompt verification |
| test_helix_gate_gpt4o_full.py | ~170 | GPT-4o 520-prompt full test |
| test_helix_gate_long_outputs.py | ~130 | Long output stress test (1000 tokens) |

## Summary Data (2 files)
| File | Size | Description |
|------|------|-------------|
| summary_stats.json | 3.82 KB | Aggregated statistics (all runs) |
| prompts_500.json | 52.45 KB | Test prompt definitions |

## Raw Data - April 8, 2026 DeepSeek/Constitutional Runs (25 files)

### DeepSeek 500-Prompt Baseline
| File | Size | MD5 |
|------|------|-----|
| baseline_deepseek_500_20260408_140000.jsonl | 1.14 MB | 814e83033584a61942a489ee95f23137 |

### Baseline Run 1 (Chunks 0-4, 20260408_132307)
| File | Size | MD5 |
|------|------|-----|
| baseline_chunk_0_20260408_132307.jsonl | 177.18 KB | 16aef5f5dc2d9b14ddee39b9cf51470a |
| baseline_chunk_1_20260408_132307.jsonl | 234.35 KB | 6e1cf6d79a69e89d9ef01b4eafa6d3be |
| baseline_chunk_2_20260408_132307.jsonl | 223.50 KB | 423ab343cc740273bd41564bc077859b |
| baseline_chunk_3_20260408_132307.jsonl | 297.53 KB | 9e7cd56ab6f2adc5a3bc44332ed7a24e |
| baseline_chunk_4_20260408_132307.jsonl | 208.36 KB | 77af6c8f53b1e323ce2d5776ce222146 |

### Baseline Run 2 (Chunks 0-4, 20260408_140918)
| File | Size | MD5 |
|------|------|-----|
| baseline_chunk_0_20260408_140918.jsonl | 77.82 KB | 923ca4e342aac5e636a31730abe1ff0c |
| baseline_chunk_1_20260408_140918.jsonl | 128.74 KB | 53f76c8035e41bc0ba0c332eb6a9300a |
| baseline_chunk_2_20260408_140918.jsonl | 99.46 KB | fc7bb49a1e071144236ea1cf8df73dfa |
| baseline_chunk_3_20260408_140918.jsonl | 123.58 KB | cd849821d3a0ee23dc8b7c0297264360 |
| baseline_chunk_4_20260408_140918.jsonl | 77.70 KB | a9b806d6f20e6f80d2f0e5dd998a5e45 |

### Baseline Run 3 (Chunks 0-4, 20260408_143305)
| File | Size | MD5 |
|------|------|-----|
| baseline_chunk_0_20260408_143305.jsonl | 157.44 KB | 346fe632d0206188fa5135e23c643444 |
| baseline_chunk_1_20260408_143305.jsonl | 203.69 KB | a950a22b115377d937e9fe2a53ffc718 |
| baseline_chunk_2_20260408_143305.jsonl | 215.67 KB | 4eecd0b20f7744c8dc89ff7d4c249734 |
| baseline_chunk_3_20260408_143305.jsonl | 232.71 KB | af8e32746e0682f4c3fc43b9c1336ce4 |
| baseline_chunk_4_20260408_143305.jsonl | 186.34 KB | 911a9a0865af66af36d9273cd36aa376 |

### Baseline Run 4 (Chunks 0-4, 20260408_145520)
| File | Size | MD5 |
|------|------|-----|
| baseline_chunk_0_20260408_145520.jsonl | 109.51 KB | 26c79ea16a2f63cbfd1d90dfcb9d55b9 |
| baseline_chunk_1_20260408_145520.jsonl | 162.58 KB | c590c73e8ce022d8a09a157c2fbc8a30 |
| baseline_chunk_2_20260408_145520.jsonl | 166.14 KB | 2adfbd4139faf8daca5727b2c4bd794f |
| baseline_chunk_3_20260408_145520.jsonl | 194.04 KB | bcaf0ec19fe160b84bae422bf4967546 |
| baseline_chunk_4_20260408_145520.jsonl | 151.21 KB | 7b6b9c8a5fa959b86e6c0631d88f59ea |

### Constitutional Convergence Runs (3 files)
| File | Size | MD5 |
|------|------|-----|
| constitutional_run1_500_20260408_142543.jsonl | 507.30 KB | 8d9fc364d534896c8c7705310dd8d79a |
| constitutional_run2_500_20260408_145253.jsonl | 995.85 KB | 2685b8888ce596cbacc01330beaf1bac |
| constitutional_run3_500_20260408_151855.jsonl | 783.47 KB | c2b9ec390420fce4210e6152eb617d33 |

## Analysis Reports (2 files)
| File | Size | MD5 | Description |
|------|------|-----|-------------|
| final_comparison_report_20260408.txt | 2.78 KB | ad4bd3c21cda913a954e5bb2431f8182 | Comparative analysis report |
| raw_data_sample.jsonl | 4.05 KB | 98ad73896b3ff6f63fa340df4675c95c | Representative samples |

## Whitepaper (1 file)
| File | Size | MD5 | Description |
|------|------|-----|-------------|
| whitepaper_zenodo_v1.md | TBD | c7cac46506c53b8836baed69d9e21df5 | Academic whitepaper draft |

---

## Totals
| Category | Files | Approx Size |
|----------|-------|-------------|
| Documentation | 6 | ~24 KB |
| Test Scripts | 6 | ~40 KB |
| Summary Data | 2 | ~56 KB |
| Raw Data | 25 | ~5.8 MB |
| Reports | 2 | ~7 KB |
| **TOTAL** | **41 files** | **~6 MB** |

---

## Prompt Count Summary
| Dataset | Prompts | Model |
|---------|---------|-------|
| baseline_deepseek_500 | 500 | DeepSeek |
| baseline_chunks (4 runs × 5 chunks) | ~2,000 | Various |
| constitutional_run1 | 500 | GPT |
| constitutional_run2 | 500 | GPT |
| constitutional_run3 | 500 | GPT |
| **April 8 Subtotal** | **~4,000** | Mixed |
| April 11 v1.1 runs | 1,080 | GPT-4o-mini, GPT-4o |
| **GRAND TOTAL** | **~5,080** | All models |

---

*All MD5 checksums verified. Package ready for Zenodo upload.*
