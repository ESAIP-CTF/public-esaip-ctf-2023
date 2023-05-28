#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

gcc -m32 -static -o chall chall.c -fno-stack-protector

mkdir -p ../dist/src 2>/dev/null

rm ../dist/chall*

cp chall ../dist/src

echo "ECTF{flag}" > ../dist/src/flag.txt

cp ../Dockerfile ../dist/
cp run_docker.sh ../dist/

cd ../dist/

zip -r chall.zip *

find ../dist/ -not -name '*.zip' -delete 2>/dev/null

md5=$(md5sum chall.zip |  sed s/\ \ chall.zip/\/g)
name="chall_$md5.zip"

mv chall.zip $name

new_content=$(sed -e "s/chall.*/$name/" ../challenge.yml)

echo -ne "$new_content" > ../challenge.yml