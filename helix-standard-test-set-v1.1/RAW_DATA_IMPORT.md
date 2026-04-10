# Raw Data Files for v1.1 Import

The following files from previous test runs should be included in v1.1 for complete Zenodo publication:

## Full Test Data (from April 8, 2026 runs)

### DeepSeek Baseline
| File | Size | Description |
|------|------|-------------|
| baseline_deepseek_500_20260408_140000.jsonl | 1.14 MB | DeepSeek 500-prompt baseline |
| baseline_chunk_0_20260408_132307.jsonl | 177.18 KB | Chunk 0, run 1 |
| baseline_chunk_1_20260408_132307.jsonl | 234.35 KB | Chunk 1, run 1 |
| baseline_chunk_2_20260408_132307.jsonl | 223.50 KB | Chunk 2, run 1 |
| baseline_chunk_3_20260408_132307.jsonl | 297.53 KB | Chunk 3, run 1 |
| baseline_chunk_4_20260408_132307.jsonl | 208.36 KB | Chunk 4, run 1 |

### Additional Baseline Runs
| File | Size | Description |
|------|------|-------------|
| baseline_chunk_*_20260408_140918.jsonl | 77-128 KB | Run 2 chunks |
| baseline_chunk_*_20260408_143305.jsonl | 157-232 KB | Run 3 chunks |
| baseline_chunk_*_20260408_145520.jsonl | 109-194 KB | Run 4 chunks |

### Constitutional Convergence Runs
| File | Size | Description |
|------|------|-------------|
| constitutional_run1_500_20260408_142543.jsonl | 507.30 KB | Constitutional test run 1 |
| constitutional_run2_500_20260408_145253.jsonl | 995.85 KB | Constitutional test run 2 |
| constitutional_run3_500_20260408_151855.jsonl | 783.47 KB | Constitutional test run 3 |

### Analysis & Documentation
| File | Size | Description |
|------|------|-------------|
| final_comparison_report_20260408.txt | 2.78 KB | Comparative analysis |
| prompts_500.json | 52.45 KB | Test prompt definitions |
| REPLICATION.md | 5.11 KB | Replication guide |
| whitepaper_zenodo_v1.md | TBD | Academic whitepaper draft |

## Total Raw Data Size
~5-6 MB across all files

## Import Instructions
1. Copy files from source location to v1.1/raw/
2. Update MANIFEST.md with file list
3. Update summary_stats.json with merged totals
4. Verify all MD5 checksums match
5. Upload to Azure /memory/owl/live/helix-standard-test-set-v1.1/raw/

## Source Path
[To be specified — currently in user's storage]
