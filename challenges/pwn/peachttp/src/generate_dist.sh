#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

gcc server.c -o server

mkdir -p ../dist/src/ 2>/dev/null

rm ../dist/chall*

cp -r websrc/ ../dist/src/
cp server ../dist/src
cp entrypoint.sh ../dist/src
cp run_docker.sh ../dist/

echo "ECTF{flag}" > ../dist/src/flag.txt

cp ../Dockerfile ../dist/

LIBC=$(ldd server | grep -oP '/.+\.6')
cp $LIBC ../dist/src/
cp $LIBC .

cd ../dist/

zip -r chall.zip *

find ../dist/ -not -name '*.zip' -delete 2>/dev/null

md5=$(md5sum chall.zip |  sed s/\ \ chall.zip/\/g)

name="chall_$md5.zip"

mv chall.zip $name

new_content=$(sed -e "s/chall.*/$name/" ../challenge.yml)

echo -ne "$new_content" > ../challenge.yml