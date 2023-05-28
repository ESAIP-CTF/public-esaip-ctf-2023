#!/bin/bash

docker build -t peachttp .
docker run -t -p 8080:8080 peachttp