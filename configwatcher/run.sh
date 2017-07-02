#!/bin/bash
set -e

CONFIG_PATH=/data/options.json

PORT=$(jq --raw-output ".port" $CONFIG_PATH)

forever -v -f --spinSleepTime=1000 --minUptime=2000  /config-watcher/watcher.js --config=${CONFIG_PATH}