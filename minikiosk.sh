#!/bin/sh

THERM_CONFIG=~/.therm_config
export THERM_CONFIG

#xset s noblank
#xset s off
xset -dpms

unclutter -idle 0.5 -root &

#matchbox-window-manager&

while true;do
    ~/thermui/therm.py
    sleep 2
done
