#!/bin/bash

docker build -t marios_sum .
docker run -t -p 55555:55555 marios_sum