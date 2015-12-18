#!/usr/bin/python
# -*- coding: utf-8 -*-

# Estructura de los paquetes que se van a construir
packages = {
    'purple-facebook': {
        'repository': 'https://github.com/jgeboski/purple-facebook.git',
        'branch': 'master',
        'prebuild-script': './autogen.sh',
        'prebuild-deps': 'mercurial ca-certificates git libglib2.0-dev libjson-glib-dev libpurple-dev zlib1g-dev'
    },
    'telegram-purple': {
        'repository': 'https://github.com/majn/telegram-purple.git',
        'branch': 'master',
        'prebuild-script': '',
        'prebuild-deps': 'git libssl-dev libglib2.0-dev libpurple-dev libwebp-dev libgcrypt-dev'
    },
    'whatsapp-purple': {
        'repository': 'https://github.com/davidgfnet/whatsapp-purple.git',
        'branch': 'master',
        'prebuild-script': '',
        'prebuild-deps': 'git libglib2.0-dev libpurple-dev libfreeimage-dev'
    }
}
