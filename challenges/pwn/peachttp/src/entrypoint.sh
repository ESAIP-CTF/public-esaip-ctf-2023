#!/bin/bash

while true; do
    /chall/server
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        # Program exited successfully, no need to restart
        exit 0
    fi

    echo "Program exited with code $exit_code. Restarting..."
    sleep 10  # Wait for 1 second before restarting
done
