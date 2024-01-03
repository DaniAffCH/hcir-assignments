#!/bin/bash 
pastPid=$(sudo lsof -i :5005 | awk '$2 ~ /^[0-9]+$/ {print $2}')
if [ -n "$pastPid" ]; then
    echo "KILLING THE PREVIOUS MODEL RASA PROCESS $pastPid"
    kill $pastPid
fi
pastPid=$(sudo lsof -i :5055 | awk '$2 ~ /^[0-9]+$/ {print $2}')
if [ -n "$pastPid" ]; then
    echo "KILLING THE PREVIOUS ACTION RASA PROCESS $pastPid"
    kill $pastPid
fi
model="20240103-120330-unary-novella.tar.gz"
cd rasa
rasa run actions &
cd ..
rasa run --model "./rasa/models/$model" --enable-api --endpoints rasa/endpoints.yml &
python3 main.py