#!/usr/bin/env bash

function wait_for(){
    local tries=0
    until $@ &> /dev/null; do
        tries=$(( $tries + 1 ))

        if [ "$tries" -ge 5 ]; then
            exit 1
        fi
    
        sleep 1
    done
}

wait_for "xhost"
wait_for "curl --fail http://127.0.0.1:5050/"

MOZ_DISABLE_CONTENT_SANDBOX=1 /opt/firefox/firefox "http://127.0.0.1:5050/"

