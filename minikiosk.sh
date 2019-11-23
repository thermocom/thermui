#!/bin/sh

THERM_CONFIG=/home/dockes/.therm_config
export THERM_CONFIG

#xset s noblank
#xset s off
xset -dpms

unclutter -idle 0.5 -root &

#matchbox-window-manager&
while true;do
    /home/dockes/thermui/therm.py
    sleep 2
done
