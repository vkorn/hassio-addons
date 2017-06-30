#!/bin/bash
set -e

CONFIG_PATH=/data/options.json

PORT=$(jq --raw-output ".port" $CONFIG_PATH)

device-locator --config=${CONFIG_PATH} --port=${PORT} --host=0.0.0.0