#!/usr/bin/env bash

exec xpra start \
    --bind-tcp 0.0.0.0:14500 \
    --html=on \
    --daemon=no \
    --pulseaudio=no \
    --speaker=yes \
    --clipboard-direction=to-client \
    --notifications=no \
    --bell=no \
    --mdns=no \
    --av-sync=yes \
    --webcam=no \
    --title="Zoomumba Container" \
    --xvfb="/usr/bin/Xvfb +extension Composite -screen 0 1920x1080x24+32 -nolisten tcp -noreset" \
    "$DISPLAY"
