#!/bin/sh

# Python libs
/usr/bin/python3 -m pip install -r /tmp/requirements.txt

# Init databasa
/usr/bin/python3 /usr/app/src/db.py

# Start bot
/usr/bin/python3 /usr/app/src/bot.py