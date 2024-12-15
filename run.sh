#!/bin/bash

race_id=$1
skip_latest=$2

docker build -t special-week-ai:latest .
docker run -v ./output:/app/output -e RACE_ID=$race_id -e SKIP_LATEST=$skip_latest special-week-ai:latest