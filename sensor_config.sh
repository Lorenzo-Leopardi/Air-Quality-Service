#!/bin/bash

sensor_name="$1"
pollutant_name="$2"
min_range="$3"
max_range="$4"

# Determine the smaller number
if (( min_range > max_range )); then
    temp="$min_range"
    min_range="$max_range"
    max_range="$temp"
fi

curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "sensor_name=$sensor_name&pollutant_name=$pollutant_name&min_range=$min_range&max_range=$max_range" \
     http://localhost:8080/sensors/$sensor_name/config