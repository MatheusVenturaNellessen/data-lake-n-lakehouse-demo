#!/usr/bin/env bash

LOG_DIR="./log"
LOG_FILE="$LOG_DIR/pipeline.txt"

mkdir -p "$LOG_DIR"

echo "[Pipeline] Starting..."

if ! python ./src/lake_pipeline.py >> "$LOG_FILE" 2>&1; then
    echo "[ERROR] Lake pipeline failed. Check $LOG_FILE"
    exit 1
fi

if ! python ./src/lakehouse_pipeline.py >> "$LOG_FILE" 2>&1; then
    echo "[ERROR] Lakehouse pipeline failed. Check $LOG_FILE"
    exit 1
fi

echo "[Pipeline] Finished successfully."