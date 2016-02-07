Django Package Builder
======================

Attention: This hasn't integrated with Django yet.

This project aims to assemble a binary (and source) package builder based on Buildbot and Django. For now it only builds debian packages compatible with Debian and its derivatives, but it will compile Fedora and Arch packages in the future.

Follow the instructions to configure django-packagebuilder for local packaging.

### Steps for using Django Package Builder

1. Install dependencies

    sudo aptitude install git virtualenv supervisor python2.7-dev apt-cacher reprepro

2. Create a new user for buildbot.

    sudo adduser buildbot

3. Configure sudo for the buildbot user. Put the following inside the ``/etc/sudoers.d/buildbot`` file (as root):

    buildbot ALL=(ALL) NOPASSWD:SETENV: ALL

4. Create a virtualenv with proper dependencies.

    su buildbot
    mkdir -p "${HOME}/buildbot"
    cd "${HOME}/buildbot"
    virtualenv --python=python2.7 virtualenv
    virtualenv/bin/pip install buildbot buildbot-slave

5. Create checkout dir.

    sudo mkdir -p /var/cache/pbuilder/git-checkout
    sudo chown -R buildbot:buildbot /var/cache/pbuilder/git-checkout

6. Create the buildbot slaves.

    virtualenv/bin/buildslave create-slave --relocatable --umask=0022 slave-sid-i386 localhost:9989 slave-sid-i386 123
    virtualenv/bin/buildslave create-slave --relocatable --umask=0022 slave-sid-amd64 localhost:9989 slave-sid-amd64 123


7. Create the buildbot master.

    git clone https://github.com/LuisAlejandro/django-packagebuilder.git master
    virtualenv/bin/buildbot upgrade-master master

8. Configure supervisor daemon for buildbot. Put the following inside the ``/etc/supervisor/conf.d/buildbot.conf`` file (as root):

    [program:buildbot-master]
    command=/home/buildbot/buildbot/virtualenv/bin/buildbot restart --nodaemon /home/buildbot/buildbot/master/
    user=buildbot

    [program:buildbot-slave-i386]
    command=/home/buildbot/buildbot/virtualenv/bin/buildslave restart --nodaemon /home/buildbot/buildbot/slave-sid-i386
    user=buildbot

    [program:buildbot-slave-amd64]
    command=/home/buildbot/buildbot/virtualenv/bin/buildslave restart --nodaemon /home/buildbot/buildbot/slave-sid-amd64
    user=buildbot

9. Create a new package repository for finished packages.

    mkdir -p /var/cache/pbuilder/repo/conf



10. Start the supervisor

    sudo service supervisor restart
