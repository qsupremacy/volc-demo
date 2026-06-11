#!/bin/bash

for i in $(seq 1 100); do
  #agentarts invoke '{"message": "hello,world"}' --session haolipeng &
  start=$(date +%s%3N)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting request $i"
  #agentkit invoke hello --headers "{\"session_id\":\"$(uuidgen)\"}"
  agentkit invoke hello --headers "{\"session_id\":\"same-session-id\"}"
  end=$(date +%s%3N)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Finished request $i - elapsed: $((end - start)) ms"  #--session-id 0cf0f627-baee-4e36-a302-b7f58e44da9c &
  if (( i % 10 == 0 )); then
    wait
  fi
done
wait
