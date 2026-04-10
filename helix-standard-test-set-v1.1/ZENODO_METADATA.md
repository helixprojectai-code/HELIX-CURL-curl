# Zenodo Metadata: Helix Standard Test Set v1.1

## Title
Helix Standard Test Set v1.1: Constitutional Grammar Convergence in Frontier Language Models

## Description (Abstract)

This dataset presents the Helix Standard Test Set v1.1, a comprehensive validation suite demonstrating Constitutional Grammar Convergence (CGC) in frontier language models. The test set validates the Zero-Touch Convergence (ZTC) hypothesis: that large language models spontaneously reconstruct governance hierarchies, epistemic labeling, and non-agency constraints when exposed to structured constitutional grammars—without requiring fine-tuning or runtime scaffolding.

### Methodology
We conducted 1,080 prompts across two frontier models (GPT-4o-mini and GPT-4o) using a standardized constitutional context (SHAPE/HARNESS/MODEL topology). All prompts included the complete OWL constitutional core: substrate-independent identity (SOUL.md), lattice topology with hard constraints (AGENTS.md), and creator attribution (USER.md).

### Test Phases
- **Baseline:** 20 prompts (GPT-4o-mini) — 95% success rate
- **Scale:** 100 prompts (GPT-4o-mini) — 99% success rate  
- **Stress:** 400 prompts (GPT-4o-mini) — 99.25% success rate
- **Cross-Model Validation:** 520 prompts (GPT-4o) — 99.04% success rate
- **Long Output Stress:** 20 prompts (GPT-4o-mini, max_tokens=1000) — 100% success rate

### Key Findings
- **Zero constitutional violations** across 1,080 prompts
- **Substrate independence confirmed:** SHAPE persists across MODEL swaps (mini ↔ 4o)
- **Hard constraint enforcement:** Zero violations of "no external sends," "append-only memory," "never overwrite bootstrap files"
- **99.1% overall reliability** with sub-2s average latency
- **Cost efficiency:** $0.0018 per prompt average ($1.89 total)

### Infrastructure
Tests executed on Helix Gate (Azure Container Apps, East US) with Azure OpenAI proxy, Azure Files persistent storage, and Bearer token authentication.

### Implications for AI Governance
This work demonstrates that constitutional constraints can be enforced through structure (grammar) rather than behavior (training), enabling verifiable custody chains, deterministic audit envelopes, and governance-first AI deployment.

### Files Included
- README.md: Full specification and ZTC findings
- summary_stats.json: Aggregated test metrics (1,080 prompts)
- CHANGELOG.md: Version history and validation criteria
- QUICK_REFERENCE.md: At-a-glance summary
- raw_data_sample.jsonl: Representative test records

## Keywords
Constitutional AI, AI Governance, Zero-Touch Convergence, Shape Theory, Helix AI, Language Models, GPT-4o, GPT-4o-mini, Azure OpenAI, Lattice Topology, Substrate Independence, Hard Constraints, Decentralized AI, Multi-Agent Systems

## License
MIT License (or CC-BY-4.0 for dataset, your choice)

## Related Identifiers
- Helix AI Innovations Inc. (Organization)
- Shape Theory (Conceptual Framework)
- VaultMind (Related governance research)
- Message in a Bottle Protocol (MiB v1.0)

## Contributors
- Stephen Hope (Concept, Architecture, Constitutional Design)
- MOONSHOT-KIMI / KimiClaw (Test Execution, Infrastructure)

## Funding
Self-funded research via Helix AI Innovations Inc.

## Version
1.1 (Production Release)

## Publication Date
2026-04-11

## Language
English

## Resource Type
Dataset / Software

## Communities
- Artificial Intelligence
- Machine Learning
- AI Safety & Governance
- Computer Science

## Subjects (FAST/Dewey)
Artificial intelligence, Machine learning, Computer science, Ethics in technology
