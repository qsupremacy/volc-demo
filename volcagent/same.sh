#!/bin/bash

for i in $(seq 1 100); do
  #agentarts invoke '{"message": "hello,world"}' --session haolipeng &
  start=$(date +%s%3N)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting request $i"

  curl  https://sd8uudap8n39pibr69fs0.apigateway-cn-beijing.volceapi.com/invoke -XPOST \
    -H "Content-Type: application/json" \
    -H "session_id: haolipeng" \
    -H "user_id: haolipeng" \
    -H "Authorization: Bearer R--Lwow2JxGko3nDWIqM--GGU_gkoUQPcfM1" \
    -d '{"prompt": "你是谁"}'

  end=$(date +%s%3N)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Finished request $i - elapsed: $((end - start)) ms"  #--session-id 0cf0f627-baee-4e36-a302-b7f58e44da9c &
  if (( i % 5 == 0 )); then
    wait
  fi
done
wait
