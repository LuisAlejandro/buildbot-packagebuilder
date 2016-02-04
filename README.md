A buildbot package builder
==========================


This project aims to assemble a binary (and source) package builder based on buildbot, to be integrated later to the [Tribus Social Network](http://tribus.readthedocs.org/). For now it only builds debian packages compatible with Debian and its derivatives, but it will compile Fedora and Arch packages in the future.

Follow the instructions to configure tribus-builder for local packaging.

###Steps for using Tribus Builder

1.- Install dependencies
    sudo aptitude install git python-virtualenv

2.- Clone the project.
    git clone https://github.com/LuisAlejandro/tribus-builder.git

2.- Create a new user for buildbot.
    sudo adduser buildbot

3.- Configure sudo for the buildbot user. Put the following inside the ``/etc/sudoers.d/buildbot`` file:
    buildbot ALL=(ALL) NOPASSWD:SETENV: ALL

4.- Create a virtualenv with proper dependencies.
    virtualenv virtualenv
    virtualenv/bin/pip install buildbot

4.- Configure supervisor daemon for buildbot. Put the following inside the ``/etc/supervisor.d/buildbot.conf`` file:
    [program:buildbot-master]
    command=/home/buildbot/buildbot/virtualenv/bin/buildbot restart --nodaemon /home/buildbot/buildbot/master/
    user=buildbot

    [program:buildbot-slave-i386]
    command=/home/buildbot/buildbot/virtualenv/bin/buildslave restart --nodaemon /home/buildbot/buildbot/slave-sid-i386
    user=buildbot

    [program:buildbot-slave-amd64]
    command=/home/buildbot/buildbot/virtualenv/bin/buildslave restart --nodaemon /home/buildbot/buildbot/slave-sid-amd64
    user=buildbot


5.- Create a new package repository for finished packages.
6.- Create buildbot slaves.
