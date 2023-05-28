#!/bin/bash

docker build -t mario_factory .
docker run -t -p 55555:55555 mario_factory