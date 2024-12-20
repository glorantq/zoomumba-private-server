#!/usr/bin/bash

until xhost &> /dev/null; do
    sleep 1
done

until pgrep "firefox" &> /dev/null; do
    sleep 1
done

echo
echo "=================================================================="
echo "The game has started successfully! To play, open $(hostname -I | cut -d' ' -f1):14500"
echo "in a browser of your choice, or, alternatively, connect to the"
echo "same host with Xpra (user: 'flash')"
echo "=================================================================="
echo
