#!/bin/bash

if [[ $(pwd) != *"pwn_my_ship/src"* ]]; then
    echo "[USAGE] You must be in pwn_my_ship/src to run the script!"
    exit
fi

# Build docker
echo -ne "\x1b[1mBuilding docker...\x1b[0m\n"
docker build -t pwn_my_ship .. #&> /dev/null

# Run & get docker id
echo -ne "\x1b[1mStarting docker...\x1b[0m\n"
docker_id=$(docker run -p 55555:55555 -d pwn_my_ship) 

# Get file
echo -ne "\x1b[1mRetrieving challenge files...\x1b[0m\n"
docker cp $docker_id:/app/bin/Debug/net7.0/win-x64/app.exe ../dist/app.exe
docker cp $docker_id:/app/bin/Debug/net7.0/win-x64/app.dll ../dist/app.dll

# Kill the docker
echo -ne "\x1b[1mStopping docker...\x1b[0m\n"
docker kill $docker_id &> /dev/null