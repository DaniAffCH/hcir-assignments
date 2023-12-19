#!/bin/bash 
pastPid=$(sudo lsof -i :5005 | awk '$2 ~ /^[0-9]+$/ {print $2}')
if [ -n "$pastPid" ]; then
    echo "KILLING THE PREVIOUS PROCESS $pastPid"
    kill $pastPid
fi
model="20231214-174915-burning-amplifier.tar.gz"
rasa run --model "./rasa/models/$model" &
python3 main.py