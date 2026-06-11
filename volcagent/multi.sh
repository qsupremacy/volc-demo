#!/bin/bash

for i in $(seq 1 100); do
  #agentarts invoke '{"message": "hello,world"}' --session haolipeng &
  time agentkit invoke hello --headers "{\"session_id\":\"$(uuidgen)\"}" &
  if (( i % 12 == 0 )); then
    wait
  fi
done
wait
