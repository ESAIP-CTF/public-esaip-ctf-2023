#!/bin/bash

sudo apt install pcscd libpcsclite-dev swig libnfc-bin qjoypad
sudo service pcscd start
sudo modprobe joydev

# disable sleep mode:
# https://raspberrytips.com/disable-sleep-mode-raspberry-pi/
sudo xset -dpms
