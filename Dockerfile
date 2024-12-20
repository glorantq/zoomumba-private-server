FROM debian:12-slim

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get upgrade -y

# Old Firefox and Flash
RUN apt-get install -y curl bzip2 libgtk-3-0 xserver-xorg-core \
    libdbus-glib-1-2 libasound2 libnss3 libssl3 libnspr4 libgtk2.0-0

WORKDIR /tmp
RUN curl -Lo firefox.tar.bz2 \
    https://archive.mozilla.org/pub/firefox/releases/84.0.2/linux-x86_64/en-GB/firefox-84.0.2.tar.bz2

RUN curl -Lo flash.tar.gz \
    https://archive.org/download/adobe-flash-player-32.0.0.465-retail-debug/flash_player_npapi_linux_debug.x86_64.tar.gz

RUN tar -xjf firefox.tar.bz2 -C /opt/

RUN mkdir -p /tmp/flash
RUN tar -xzf flash.tar.gz -C /tmp/flash
RUN cp -rfn /tmp/flash/usr /

RUN mkdir -p /usr/lib/mozilla/plugins
RUN cp /tmp/flash/libflashplayer.so /usr/lib/mozilla/plugins

RUN rm -rf /tmp/firefox.tar.bz2 /tmp/flash.tar.gz /tmp/firefox /tmp/flash

# Isolated X11
RUN curl -o /usr/share/keyrings/xpra.asc https://xpra.org/xpra.asc
RUN curl -Lo /etc/apt/sources.list.d/xpra.sources \
    https://raw.githubusercontent.com/Xpra-org/xpra/master/packaging/repos/bookworm/xpra.sources

RUN apt-get update -y
RUN apt-get install -y xpra xvfb dbus-x11 supervisor pulseaudio \
    pulseaudio-utils tini gstreamer1.0-plugins-base \
    gstreamer1.0-x gstreamer1.0-gtk3 gstreamer1.0-pulseaudio \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly python3-gst-1.0 x11-xserver-utils

# Python for the project
RUN apt-get install -y python3 python3-pip python3-flask

# Drop privileges
RUN useradd -ms /bin/sh -u 1000 flash
RUN mkdir -p /run/user/1000
RUN mkdir -p /run/xpra
RUN chown flash:flash /run/user/1000
RUN chown flash:flash /run/xpra

# Project files
ADD --chown=flash:flash ./docker /docker
ADD ./docker/etc /etc

ADD --chown=flash:flash . /project

WORKDIR /

# Flash timebomb
RUN apt-get install -y bbe
RUN /docker/remove-flash-timebomb.sh /usr/lib/mozilla/plugins/libflashplayer.so

# Flash config
RUN cp /docker/home/mm.cfg /home/flash/

ENTRYPOINT [ "/bin/tini", "--" ]
CMD [ "/bin/supervisord", "-c", "/etc/supervisord.conf" ]

