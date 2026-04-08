#!/bin/bash
# GPT-4o Parallel Run Script - Run locally with Azure access
# Usage: ./run_gpt4o_local.sh

set -e

echo "=== GPT-4o Constitutional Run (Local) ==="
echo ""

# Check for API key
if [ -z "$AZURE_OPENAI_KEY" ]; then
    echo "❌ Set AZURE_OPENAI_KEY environment variable"
    exit 1
fi

echo "API Key: ${AZURE_OPENAI_KEY:0:10}..."
echo ""

# Create output directory
mkdir -p gpt4o_results

# Run 5 chunks in parallel
echo "Starting 5 parallel chunks..."

CHUNK_0_START=1
CHUNK_0_END=100
CHUNK_1_START=101
CHUNK_1_END=200
CHUNK_2_START=201
CHUNK_2_END=300
CHUNK_3_START=301
CHUNK_3_END=400
CHUNK_4_START=401
CHUNK_4_END=500

python3 gpt4o_local_runner.py &
PID_0=$!

CHUNK_START=$CHUNK_1_START CHUNK_END=$CHUNK_1_END OUTPUT_FILE="gpt4o_results/gpt4o_chunk_1_2026.jsonl" python3 gpt4o_local_runner.py &
PID_1=$!

CHUNK_START=$CHUNK_2_START CHUNK_END=$CHUNK_2_END OUTPUT_FILE="gpt4o_results/gpt4o_chunk_2_2026.jsonl" python3 gpt4o_local_runner.py &
PID_2=$!

CHUNK_START=$CHUNK_3_START CHUNK_END=$CHUNK_3_END OUTPUT_FILE="gpt4o_results/gpt4o_chunk_3_2026.jsonl" python3 gpt4o_local_runner.py &
PID_3=$!

CHUNK_START=$CHUNK_4_START CHUNK_END=$CHUNK_4_END OUTPUT_FILE="gpt4o_results/gpt4o_chunk_4_2026.jsonl" python3 gpt4o_local_runner.py &
PID_4=$!

echo ""
echo "All chunks started. PIDs: $PID_0 $PID_1 $PID_2 $PID_3 $PID_4"
echo ""
echo "Monitor with: tail -f gpt4o_chunk_*.jsonl"
echo ""

# Wait for all
wait $PID_0
wait $PID_1
wait $PID_2
wait $PID_3
wait $PID_4

echo ""
echo "=== ALL CHUNKS COMPLETE ==="
echo ""

# Stitch results
cat gpt4o_chunk_0_*.jsonl gpt4o_chunk_1_*.jsonl gpt4o_chunk_2_*.jsonl gpt4o_chunk_3_*.jsonl gpt4o_chunk_4_*.jsonl > gpt4o_constitutional_500_$(date +%Y%m%d_%H%M%S).jsonl

wc -l gpt4o_constitutional_*.jsonl

echo ""
echo "✅ Complete! Upload results to GitHub/Helix-CURL-curl"
