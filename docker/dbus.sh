#!/usr/bin/env bash

mkdir -p /var/run/dbus
dbus-uuidgen > /var/lib/dbus/machine-id
exec dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address --nofork

