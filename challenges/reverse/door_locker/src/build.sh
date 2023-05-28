#!/bin/bash
# compile on x64 linux

nasm door_locker.s -g -f elf64 -o door_locker.o
ld door_locker.o -o door_locker
objdump.exe -M intel -d door_locker
