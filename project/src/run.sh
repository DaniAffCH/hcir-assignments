#!/bin/bash 
pastPid=$(sudo lsof -i :5005 | awk '$2 ~ /^[0-9]+$/ {print $2}')
if [ -n "$pastPid" ]; then
    echo "KILLING THE PREVIOUS PROCESS $pastPid"
    kill $pastPid
fi
model="20231220-190630-abstract-swing.tar.gz"
rasa run --model "./rasa/models/$model" --enable-api &
python3 main.py