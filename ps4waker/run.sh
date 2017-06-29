#!/bin/bash
set -e

CONFIG_PATH=/data/options.json
FINAL_CONFIG=/data/ps4-creds.json

PORT=$(jq --raw-output ".port" $CONFIG_PATH)

mustache ${CONFIG_PATH} /templates/template.json > ${FINAL_CONFIG}

ps4-hassio-waker --credentials=${FINAL_CONFIG} --port=${PORT} --host=0.0.0.0