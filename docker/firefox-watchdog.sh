#!/usr/bin/env bash

until pgrep "firefox" &> /dev/null; do
    sleep 3
done

function attempt_container_stop(){
    sleep 5

    if ! pgrep "firefox" &> /dev/null; then
        echo "Firefox seems to be shut down, stopping container..."
        supervisorctl -c /etc/supervisord.conf shutdown
        exit 0
    fi
}

while pgrep "supervisor" &> /dev/null; do
    while pgrep "firefox" &> /dev/null; do
        sleep 5
    done

    attempt_container_stop
done
